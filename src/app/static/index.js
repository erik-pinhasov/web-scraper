var reqInProgress = false;

$(document).ready(function() {
    var brand;
    $(document).on('click', ".brand-image", function() {
        brand = $(this).data('brand');
        updateModels(brand);
    });

    $(document).on('click', "#models-menu input[name='model']", function() {
        getComparison(brand, $(this).val());
    });
});

function updateModels(brand) {
    $.get("/get_models", { brand: brand }, function(data) {
        var modelsMenuDiv = $("#models-menu");
        var modelCon = $("#model-container")
        modelsMenuDiv.empty();

        $.each(data.models, function(index, model) {
            modelsMenuDiv.append('<input id="model-button" type="button" name="model" value="' + model + '">');
        });
        modelCon.show();
    });
}

function getComparison(brand, model) {
    if (reqInProgress) {
        return;
    }

    reqInProgress = true;
    $("#result-table").empty();
    $(".loader").show();

    $.get("/get_comparison", { brand, model }, function(data) {
        var title = `<h3>Results for ${brand} ${model}</h3>`;
        var table = createTable(data);
        $(".loader").hide();
        $("#result-table").append(title, table);

        reqInProgress = false;
    });
}


function createTable(data) {
    var table = $('<table>');
    var thead = $('<thead>').appendTo(table);
    var tbody = $('<tbody>').appendTo(table);
    createHeaderRow(thead);
    createProductRows(data, tbody);
    return table;
}

function createHeaderRow(thead) {
    var headerRow = $('<tr>').appendTo(thead);
    headerRow.append('<th>Storage + RAM</th>');

    var websites = ['ksp', 'ivory', 'bug'];
    for (var i = 0; i < websites.length; i++) {
        var logo = '/static/images/' + websites[i] + '_logo.png';
        headerRow.append(`<th><img src="${logo}" alt="${websites[i]}"></th>`);
    }
}

function createProductRows(data, tbody) {
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            var product = data[key];
            var row = $('<tr>').appendTo(tbody);
            row.append('<td>' + key + '</td>');
            createPriceRow(product, row);
        }
    }
}

function createPriceRow(product, row) {
    var websites = ['ksp', 'ivory', 'bug'];
    for (var i = 0; i < websites.length; i++) {
        var website = websites[i];
        var price = product[website + '_price'];
        var url = product[website + '_url'];
        var toInsert = '<td>' + (price ? price + ' ₪': 'Out of stock') +
                        (url ? `<br><a href="${url}" target="_blank">Product Link</a>` : '') + '</td>';
        row.append(toInsert);
    }
}