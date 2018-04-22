$(document).ready(function () {

	//console.log(ajax_get_hotels);

/*
	var clients = [
        { "Name": "Otto Clay", "Age": 25, "Country": 1, "Address": "Ap #897-1459 Quam Avenue", "Married": false },
        { "Name": "Connor Johnston", "Age": 45, "Country": 2, "Address": "Ap #370-4647 Dis Av.", "Married": true },
        { "Name": "Lacey Hess", "Age": 29, "Country": 3, "Address": "Ap #365-8835 Integer St.", "Married": false },
        { "Name": "Timothy Henson", "Age": 56, "Country": 1, "Address": "911-5143 Luctus Ave", "Married": true },
        { "Name": "Ramona Benton", "Age": 32, "Country": 3, "Address": "Ap #614-689 Vehicula Street", "Married": false }
    ];
 
    var countries = [
        { Name: "", Id: 0 },
        { Name: "United States", Id: 1 },
        { Name: "Canada", Id: 2 },
        { Name: "United Kingdom", Id: 3 }
    ];
 
    $("#jsGrid").jsGrid({
        width: "100%",
        height: "400px",
 
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
 
        data: clients,
 
        fields: [
            { name: "Name", type: "text", width: 150, validate: "required" },
            { name: "Age", type: "number", width: 50 },
            { name: "Address", type: "text", width: 200 },
            { name: "Country", type: "select", items: countries, valueField: "Id", textField: "Name" },
            { name: "Married", type: "checkbox", title: "Is Married", sorting: false },
            { type: "control" }
        ]
    });

*/



        $("#jsGrid").jsGrid({
            height: "400px",
            width: "100%",
            filtering: true,
            inserting: true,
            editing: true,
            sorting: true,
            paging: true,
            autoload: true,
            pageSize: 10,
            pageButtonCount: 5,
            deleteConfirm: "Удалить выбранную запись?",
            controller: {
                loadData: function(filter) {
                    var d = $.Deferred();
                    $.ajax({
                        type: "GET",
                        contentType: "application/json; charset=utf-8",
                        url: ajax_get_hotels,
                        data: filter
                    }).done(function(result) {
                    	//console.log(result[1].fields.name);
                        d.resolve($.map(result, function(item) {
                            return $.extend(item.fields, { id: item.pk });
                        }));
                    });
                    return d.promise();
                },
                insertItem: function(item) {
                    return $.ajax({
                        type: "POST",
                        url: "",
                        data: item
                    });
                },
                updateItem: function(item) {
                    return $.ajax({
                        type: "PUT",
                        url: "" + item.id,
                        data: item
                    });
                },
                deleteItem: function(item) {
                    return $.ajax({
                        type: "DELETE",
                        url: "" + item.id
                    });
                }
            },
            fields: [
                { name: "name", title: "Наименование", type: "text", width: 150 },
                { name: "manager", type: "text", width: 50, filtering: false },
                { type: "control"},
            ]
            
        });




});
