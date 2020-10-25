function showcost(checked) {
    if (checked == true) {
        $("#zvat").show();
        $("#bezvat").hide();
    } else {
        $("#zvat").hide();
        $("#bezvat").show();
    }
}

function onCheckboxChanged(checked) {
    if (checked == true) {
        $("#HiddenCompany").show();
    } else {
        $("#HiddenCompany").hide();
    }
}