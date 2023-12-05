var req_in_progress = false;

$(document).ready(function() {
    var current_brand;

    // Brand selection
    $(document).on('click', ".brand-image", function() {
        $("#result-table").empty();
        current_brand = $(this).data('brand');
        update_models(current_brand);
        scroll_down();
    });

    // Model selection
    $(document).on('click', "#model-container input[name='model']", function() {
        get_comparison(current_brand, $(this).val());
        scroll_down();
    });
});

// Update models based on selected brand
function update_models(brand) {
    $("#select-model").show();
    $.get("/get_models", { brand: brand }, function(data) {
        var model_container = $("#model-container");
        model_container.empty()

        $.each(data.models, function(index, model) {
            model_container.append('<input id="model-button" type="button" name="model" value="' + model + '">');
        });
        model_container.show();
    });
}

// Get comparison results
function get_comparison(brand, model) {
    if (req_in_progress) {
        return;
    }

    req_in_progress = true;
    $("#result-table").empty();
    $(".loader").show();

    $.get("/get_comparison", { brand, model }, function(data) {
        var title = `<h2 style="font-size: 1.8em;">Results for ${brand} ${model}</h2>`;
        var table = create_table(data);
        $(".loader").hide();
        $("#result-table").append(title, table);
        scroll_down();
        req_in_progress = false;
    });
}

// Create the comparison table
function create_table(data) {
    var table = $('<table>');
    var thead = $('<thead>').appendTo(table);
    var tbody = $('<tbody>').appendTo(table);
    create_header_row(thead);
    create_product_rows(data, tbody);
    return table;
}

// Create the header row of the table
function create_header_row(thead) {
    var header_row = $('<tr>').appendTo(thead);
    header_row.append('<th>Storage + RAM</th>');

    var websites = ['ksp', 'ivory', 'bug'];
    for (var i = 0; i < websites.length; i++) {
        var logo = '/static/images/' + websites[i] + '_logo.png';
        header_row.append(`<th><img src="${logo}" alt="${websites[i]}"></th>`);
    }
}

// Create rows for each product in the table
function create_product_rows(data, tbody) {
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            var product = data[key];
            var row = $('<tr>').appendTo(tbody);
            row.append('<td>' + key + '</td>');
            create_price_row(product, row);
        }
    }
}

// Create the price row for each product
function create_price_row(product, row) {
    var websites = ['ksp', 'ivory', 'bug'];
    for (var i = 0; i < websites.length; i++) {
        var website = websites[i];
        var price = product[website + '_price'];
        var url = product[website + '_url'];
        var to_insert = '<td>' + (price ? price + ' ₪': 'Out of stock') +
                        (url ? `<br><a href="${url}" target="_blank">Product Link</a>` : '') + '</td>';
        row.append(to_insert);
    }
}

function scroll_down() {
    $('html, body').animate({
        scrollTop: $(document).height()
    }, 1000);
}