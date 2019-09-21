import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/js/dist/collapse.js';
import 'datatables.net';
import 'datatables.net-bs4';
import 'datatables.net-bs4/css/dataTables.bootstrap4.css';
import 'datatables.net-buttons';
import 'datatables.net-buttons-bs4';
import 'datatables.net-buttons-bs4/css/buttons.bootstrap4.css';
import 'datatables.net-buttons/js/buttons.colVis.js';
import 'datatables.net-fixedheader';
import 'datatables.net-fixedheader-bs4';
import 'datatables.net-fixedheader-bs4/css/fixedHeader.bootstrap4.css';
import 'datatables.net-responsive';
import 'datatables.net-responsive-bs4';
import 'datatables.net-responsive-bs4/css/responsive.bootstrap4.css';
import $ from 'jquery';
import '../css/style.css';

$(document).ready(function () {
    var tableid = 'main_table';
    var countdownid = 'countdown-value';

    if (document.getElementById(tableid)) {
        $('#' + tableid).DataTable({
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
    }
    if (document.getElementById(countdownid)) {
        (function countdown(remaining) {
            if (remaining <= 0)
                location.reload(true);
            document.getElementById(countdownid).innerHTML = remaining;
            setTimeout(function () {
                countdown(remaining - 1);
            }, 1000);
        })(120);
    }
});