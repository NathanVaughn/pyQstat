// external javascript
var $ = require('jquery');
require('popper.js');
require('bootstrap');
require('datatables.net');
require('datatables.net-bs4');
require('datatables.net-buttons');
require('datatables.net-buttons/js/buttons.colVis.js');
require('datatables.net-buttons-bs4');
require('datatables.net-fixedheader');
require('datatables.net-fixedheader-bs4');
require('datatables.net-responsive');
require('datatables.net-responsive-bs4');

// external css
require('bootstrap/dist/css/bootstrap.css');
require('datatables.net-bs4/css/dataTables.bootstrap4.css');
require('datatables.net-buttons-bs4/css/buttons.bootstrap4.css');
require('datatables.net-fixedheader-bs4/css/fixedheader.bootstrap4.css');
require('datatables.net-responsive-bs4/css/responsive.bootstrap4.css');

// our css
require('./../css/style.css');

$(document).ready(function () {
    $('#main_table').DataTable({
        responsive: true,
        autoWidth: false,
        fixedHeader: true,
        order: ordering,
        dom: 'Bfrtip',
        pagingType: 'numbers',
        buttons: {
            dom: {
                container: {
                    className: 'dt-buttons btn-group float-left'
                }
            },
            buttons: ['pageLength', 'colvis']
        },
    });
});