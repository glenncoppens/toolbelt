({
    invoke : function(component, event, helper) {
        // Get the "url" attribute
        var url = component.get("v.url");

        if ((typeof sforce != 'undefined') && sforce && (!!sforce.one)) {
            sforce.one.navigateToURL(url);
        } else {
            window.location.assign(url);
        }
    }
})