$(document).ready(function(){
    //var state = true;
    inittable();
    $(".byidb").click(function () {
        if(this.value === "1"){
            addlength(1,this.id);
            Init2();
            this.value = "0";
        }
        else{
            addlength(-1,this.id);
            Init2();
            this.value = "1";
        }
    });
    $("#srhbyid").click(function(){
        $("#srhbyid-d").slideToggle("fast");
    });
    $("#srhbyname").click(function(){
        $("#srhbyname-d").slideToggle("fast");
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
         $.ajax({
           type: "post",
           url: "/Drug/ProjectionResult/",
           data:{
             "drug":JSON.stringify(index)
           },
           dataType:"json",
            success:function(data){
               datax = reversedata(data);
                refreshTable(datax);
            },
            fail: function () {
                alert("Disconnect!");
            },
        });

        //state = !state;
    });
});

function delNrows(data,table) {
        var selection = table.getSelected();
        var col = selection[0][1];
        console.log(col);
        console.log(data.length);
        for(i = 0;i < data.length;i++){
            console.log(data[i][col]);
            if(data[i][col] === ""){
                data.splice(i,1);
                i--;
            }
            console.log(data[i]);
            console.log(data);
        }
        refreshTable(data);
    }

function inittable() {
    var datac = [
            ["1","1","1","1","1","1","1","","1","1","1","1"],
            ["1","1","1","1","1","1","1","1","1","1","1","1"],
            ["1","1","1","1","1","","1","1","1","1","1","1"],
            ["1","1","1","1","1","1","1","1","1","1","1","1"],
            ["","1","1","1","1","1","1","1","","1","1","1"],
            ["","1","1","1","1","1","1","1","1","1","1","1"],
        ],
        container;
    datax = datac;

    function firstRowRenderer(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.color = 'black';
        td.style.background = '#37c6c0';
    }

    container = document.getElementById('table');
     var table = new Handsontable(container, {
         data: datac,
         width: 0.6*window.innerWidth,
         height:0.9*window.innerHeight,
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
         minCols: 20,
         minRows: 30,
         maxCols: 20,
         maxRows: 1000,
         readOnly: true,
         manualColumnFreeze: true,
         contextMenu:{
             callback: function (key,selection,clickEvent) {
                 console.log(clickEvent);
             },
             items:{
                 "about":{
                     name:'Delete Null Rows',
                     callback: function(){
                         setTimeout(delNrows(datac,table),0);
                     }
                 }
             }
         },
    });
}
function refreshTable(data) {
    var container,datac = data;

    function firstRowRenderer(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.color = 'black';
        td.style.background = '#37c6c0';
    }

    container = document.getElementById('table');
    var table = new Handsontable(container, {
        data: datac,
        width: window.innerWidth,
        height:0.9*window.innerHeight,
        autoRowSize: true,
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
        readOnly: true,
        manualColumnFreeze: true,
        autoInsertRow:true,
        contextMenu:{
             callback: function (key,selection,clickEvent) {
                 console.log(clickEvent);
             },
             items:{
                 "about":{
                     name:'Delete Null Rows',
                     callback: function(){
                         setTimeout(delNrows(datac,table),0);
                     }
                 }
             }
         },
    });
}
function reversedata(data) {
    var datac = new Array();
    for( k = 0,klen = data[index[0]].length+1;k<klen;k++)
        datac[k] = new Array();
    datac[0] = index;
    console.log(data[0]);
    console.log(data[index[0]][0]);
    console.log(data[index[0]].length);
    for(j = 0,len=index.length; j < len; j++)
        for(i = 1,ilen = data[index[0]].length+1;i < ilen;i++)
            datac[i].push(data[index[j]][i]);
    return datac;
}