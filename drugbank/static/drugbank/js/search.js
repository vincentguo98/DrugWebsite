$(document).ready(function () {
    $("#drugbank-drug-type-label").html("drug type");
    $("#drugbank-drug-group-label").html("drug group");
    $(".minop").click(function () {
        if (this.value == "0") {
            index.push(this.id);
            this.value = "1";
            var a1 = this.firstChild;
            a1.innerHTML += "<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>";
        } else {
            this.value = "0";
            var a2 = this.firstChild;
            a2.innerHTML = a2.innerText;
            var i = index.indexOf(this.id);
            index.splice(i, 1);
        }
        // drug = { "drugindex":index[0]}
        $.ajax({
            type: "post",
            url: "/Drug/ProjectionResult/",
            data: {
                "drug": JSON.stringify(index)
            },
            dataType: "json",
            success: function (data) {
                datax = reversedata(data);
                refreshTable(datax);
                refreshcolunms();
            },
            fail: function () {
                alert("Disconnect!");
            },
        });
    });
    $(".dropdown-menu").on('click', function (e) {
        e.stopPropagation();
    });
    $("#drugbank-drug-div").on("change", function () {
        $("#drugbank-drug-div option").each(function () {
            val = $(this).html();
            if (val == "drug-drug interaction")
                val = "drug-drug-interaction";
            if (val != "smile" && val != "inchi") {
                if ($(this).get(0).selected) {
                    $("#drugbank-" + val + "-div").show();
                } else {
                    $("#drugbank-" + val + "-div").hide();
                }
            }
        });
    });

    $("#drugbank-drug-div").val("1");
    $("#drugbank-drug-type-div").val("3");
    $("#drugbank-drug-group-div").val("8");
    $("#drugbank-fingerprint-selector").val("2");
    $("#drugbank-download-selector").val("1");



    $(".download").on('click', function(){
        cond = {};
        cond.drug = []
        cond.drug_group = []
        $("#drugbank-drug-div option").each(function () {
            val = $(this).html();
            if ($(this).get(0).selected){
                cond.drug.push(val);
            }
        });
        $("#drugbank-drug-type-div option").each(function () {
            val = $(this).html();
            if ($(this).get(0).selected){
                cond.drug_type = val;
            }
        });
        $("#drugbank-drug-group-div option").each(function () {
            val = $(this).html();
            if ($(this).get(0).selected){
                cond.drug_group.push(val);
            }
        });
        $("#drugbank-fingerprint-div option").each(function () {
            val = $(this).html();
            if ($(this).get(0).selected){
                if (val == "yes")
                    cond.fingerprint = 1 ;
                else
                    cond.fingerprint = 0;
            }
        });
        $("#drugbank-download-div option").each(function () {
            val = $(this).html();
            if ($(this).get(0).selected){
                cond.download = val;
            }
        });
        $.ajax({
            type: "post",
            url: "../filter/",
            data: cond,
            traditional:true,
            dataType: "json",
            success: function (response) {
                alert("开始下载");
                window.location.href = "../download/"
            }
        });
    });
});
