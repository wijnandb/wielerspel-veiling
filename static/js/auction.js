        function addRider(identifier) {
            //alert('sanity check');
            let riderID = $(identifier).data('rider');
            var amount = document.getElementById("value-"+riderID).value;  
            //alert("Punten:"+amount);
            //alert("rennerID:"+riderID);
            
            
            $.ajax({
                url: '{% url "auction:ajax-add-rider-tobeauctioned" %}',
                type: 'POST',
                headers: {
                    "X-CSRFToken": '{{ csrf_token }}',
                },
                data: {
                    'riderID': riderID,
                    'amount': amount,
                },
                success: function(json){
                    console.log(json);
                    document.getElementById("row-"+riderID).className = "table-success";
                    document.getElementById("button-"+riderID).textContent = "bijwerken";
                },
                error: function (json) {
                    //location.reload();
                    console.log(json);
                }
            });
        };

        function sellRider(identifier) {
            let riderID = $(identifier).data('rider');

            $.ajax({
                url: '{% url "auction:ajax-set-rider-to-sold" %}',
                type: 'POST',
                headers: {
                    "X-CSRFToken": '{{ csrf_token }}',
                },
                data: {
                    'riderID': riderID,
                },
                success: function(json){
                    console.log(json);
                    //document.getElementById("row-"+riderID).className = "table-success";
                    //document.getElementById("button-"+riderID).textContent = "bijwerken";
                },
                error: function (json) {
                    //location.reload();
                    console.log(json);
                }
            });
        };

<script type="text/javascript" src="https://cdn.datatables.net/v/bs4/dt-1.10.22/datatables.min.js"></script>


    $(document).ready( function () {
        $('#renners').DataTable( {
            "dom": '<"top"if>rt<"bottom"lp><"clear">',
            "pageLength": 50,
            "language": {
                "sProcessing": "Bezig...",
                "sLengthMenu": "_MENU_ resultaten weergeven",
                "sZeroRecords": "Geen resultaten gevonden",
                "sInfo": "_START_ tot _END_ van _TOTAL_ resultaten",
                "sInfoEmpty": "Geen resultaten om weer te geven",
                "sInfoFiltered": " (gefilterd uit _MAX_ resultaten)",
                "sInfoPostFix": "",
                "sSearch": "Zoeken:",
                "sEmptyTable": "Geen resultaten aanwezig in de tabel",
                "sInfoThousands": ".",
                "sLoadingRecords": "Een moment geduld aub - bezig met laden...",
                "oPaginate": {
                    "sFirst": "Eerste",
                    "sLast": "Laatste",
                    "sNext": "Volgende",
                    "sPrevious": "Vorige"
                },
            }
        } );
    } );

