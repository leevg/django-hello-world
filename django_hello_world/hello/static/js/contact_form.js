jQuery(function() {
    var form = jQuery("#UserInfoForm");
    form.submit(function(e) {
        jQuery("#id_send").attr('disabled', true)
        var array = form.serializeArray()
        form.find(':input:not(:disabled)').prop('disabled',true)
        jQuery("#status").prepend('<span>Saving changes, please wait</span>')
        jQuery("#ajax").load(
            form.attr('action') + ' #ajax',
            array,
            function(responseText, responseStatus) {
                jQuery("#id_send").attr('disabled', false)

                if (responseText == 'success'){
                    alert('User info saved!')
                    window.location = '/'
                }
            }
        );
        e.preventDefault();
    });
});