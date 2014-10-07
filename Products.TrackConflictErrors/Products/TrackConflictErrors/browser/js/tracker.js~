$(document).ready(function(){

	$("input[name='form.button.clearTracker']").click(function (e) {
            e.preventDefault();
            var auth=$('input[name="_authenticator"]').val();
            $.ajax({
                type: "POST",
                url: '@@tracker-clear',
                data: "_authenticator="+auth,
                success: function (msg) {
                       location.reload();
                    
                },
                error: function (msg) {
                    alert("Error sending AJAX request at tracker-clear:" );
                }
            });
        });
        $("input[name='form.button.refresh']").click(function (e) {
            e.preventDefault();
            location.reload();
        });

});
