$(document).ready(function(){
    //var state = true;
    inittable();
    $(".byidb").click(function () {
        if(this.value === "1"){
            ch = canvas.height = ch + 70;
            cy = ch/2;
            Init2();
            this.value = "0";
        }
        else{
            ch = canvas.height = ch - 70;
            cy = ch/2;
            Init2();
            this.value = "1";
        }
    });
    $(".srhbyid").click(function(){
        $(".srcbyid-d").slideToggle("fast");
    });
    $(".srhbyname").click(function(){
        $(".srcbyname-d").slideToggle("fast");
    });
    $(".opbutton").click(function () {
        var id = this.id
        console.log(id)
        if(this.value === "1")
        {
            $("#"+id).animate({
                backgroundColor: "#5cb85c",
                borderColor: "#5cb85c",
                color: "#fff",
                value: "0",
            }, "fast" );
            $("#"+id+"-sel").animate({
                backgroundColor: "#5cb85c",
                borderColor: "#5cb85c",
                color: "#fff",
            },"fast");
            var arr = document.getElementsByClassName(id+"-list");
            for(var j = 0,len=arr.length; j < len; j++) {
                if(arr[j].value == "0"){
                    arr[j].value = "1";
                    index.push(arr[j].id);
                    var a1 = arr[j].firstChild;
                    a1.innerHTML += "<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>";
                }
            }
        }
        else
        {
            $("#"+id).animate({
                backgroundColor: "#337ab7",
                borderColor: "#337ab7",
                color: "#fff",
                value: "1",
            }, "fast" );
            $("#"+id+"-sel").animate({
                backgroundColor: "#337ab7",
                borderColor: "#337ab7",
                color: "#fff",
                value: "1",
            }, "fast" );
            var arr2 = document.getElementsByClassName(id+"-list");
            for(var j = 0,len=arr2.length; j < len; j++) {
                if(arr2[j].value == "1"){
                    arr2[j].value = "0";
                    var a2 = arr2[j].firstChild;
                    a2.innerHTML = a2.innerText;
                    var i = index.indexOf(arr2[j].id);
                    index.splice(i,1);
                }
            }
        }
        //state = !state;
    });
});

function inittable() {
    var data = [
            ["","","","","","","","","","","",""],
        ],
        container;

    function firstRowRenderer(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.color = 'black';
        td.style.background = '#37c6c0';
    }

    container = document.getElementById('table');
     var table1 = new Handsontable(container, {
         data: data,
         width: 720,
         height:650,
         rowHeights: 25,
         colWidths: 60,
        afterSelection: function (row, col, row2, col2) {
            var meta = this.getCellMeta(row2, col2);

            if (meta.readOnly) {
                this.updateSettings({fillHandle: false});
            }
            else {
                this.updateSettings({fillHandle: true});
            }
        },
        cells: function (row, col) {
            var cellProperties = {};
            var data = this.instance.getData();

            if (row === 0) {
                cellProperties.renderer = firstRowRenderer;
            }
            return cellProperties;
        },
         maxCols: 20,
         maxRows: 1000,
         readOnly: true,
         manualColumnFreeze: true,
    });
}
function refreshTable(data) {
    var container,
    datac = data;

    function firstRowRenderer(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.color = 'black';
        td.style.background = '#37c6c0';
    }

    container = document.getElementById('table');
    var table1 = new Handsontable(container, {
        data: datac,
        width: 720,
        height:650,
        rowHeights: 25,
        colWidths: 60,
        afterSelection: function (row, col, row2, col2) {
            var meta = this.getCellMeta(row2, col2);

            if (meta.readOnly) {
                this.updateSettings({fillHandle: false});
            }
            else {
                this.updateSettings({fillHandle: true});
            }
        },
        cells: function (row, col) {
            var cellProperties = {};
            var datac = this.instance.getData();

            if (row === 0) {
                cellProperties.renderer = firstRowRenderer;
            }
            return cellProperties;
        },
        maxCols: 20,
        maxRows: 1000,
        readOnly: true,
        manualColumnFreeze: true,
    });
}