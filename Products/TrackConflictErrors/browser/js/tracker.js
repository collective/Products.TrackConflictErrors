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
        $("input[name='form.button.startTracker']").click(function (e) {
            e.preventDefault();
            var auth=$('input[name="_authenticator"]').val();
            $.ajax({
                type: "POST",
                url: '@@tracker-start',
                data: "_authenticator="+auth+"&startbutton="+'yes',
                success: function (msg) {
                       $("input[name='form.button.startTracker']").attr('disabled','disabled');
                       $("input[name='form.button.stopTracker']").removeAttr('disabled');
                       location.reload();
                    
                },
                error: function (msg) {
                    alert("Error sending AJAX request at tracker-start:" );
                }
            });
        });
        $("input[name='form.button.refresh']").click(function (e) {
            e.preventDefault();
            var auth=$('input[name="_authenticator"]').val();
            $.ajax({
                type: "POST",
                url: '@@tracker-start',
                data: "_authenticator="+auth+"&refreshbutton="+'yes',
                success: function (msg) {
                       
                       location.reload();
                    
                },
                error: function (msg) {
                    alert("Error sending AJAX request at tracker-start:" );
                }
            });
        });
       
        $("input[name='form.button.stopTracker']").click(function (e) {
            e.preventDefault();
            var auth=$('input[name="_authenticator"]').val();
            $.ajax({
                type: "POST",
                url: '@@tracker-start',
                data: "_authenticator="+auth+"&closebutton="+'yes',
                success: function (msg) {
                       $("input[name='form.button.stopTracker']").attr('disabled','disabled');
                       $("input[name='form.button.startTracker']").removeAttr('disabled');
                       location.reload();
                    
                },
                error: function (msg) {
                    alert("Error sending AJAX request at tracker-start:" );
                }
            });
        });
});
