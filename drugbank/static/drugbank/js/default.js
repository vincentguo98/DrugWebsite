var tablex;
$(document).ready(function(){
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
                refreshcolunms();
            },
            fail: function () {
                alert("Disconnect!");
            },
        });
    });
    $("#srhbykey-g").click(function () {
        var contain = document.getElementById("srhbykey-b");
        var selected = contain.innerText;
        var input = document.getElementById("srhbykey-i");
        var col = datax[0].indexOf(selected);
        for(i = 1;i<datax.length-1;i++){
            if(datax[i][col].indexOf(input.value) === -1){
                datax.splice(i,1);
                i--;
            }
        }
        input.value = "";
        refreshTable(datax);
    });
    $("#undo").click(function () {
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
                refreshcolunms();
            },
            fail: function () {
                alert("Disconnect!");
            },
        });
        var input = document.getElementById("srhbykey-i");
        input.value = "";
    });
    $(".mindown").click(function () {
        var format = this.id;
        console.log(format);
        var datad = new Array();
        for(var i=0;i<datax[0].length;i++)
        {
            var list = new Array();
            for(var j=1;j<datax.length-1;j++) {
                list.push(datax[j][i]);
            }
            var hello = new Object();
            eval("hello."+datax[0][i]+"=list;");
            datad.push(hello);
        }
        console.log(datad);
        console.log(JSON.stringify(datad))
        $.ajax({
           type: "post",
           url: "/Drug/download/",
           data:{
                "download_content":JSON.stringify(datad),
                "format_string":format,
           },
           // dataType:"json",
            success:function(data){
                alert("Start Download！");
                if (data == "json"){
                    window.location.href="../jsonfiledownload";
                }
                if (data == "csv"){
                    window.location.href="../csvfiledownload";
                }
                if (data == "txt"){
                    window.location.href="../txtfiledownload"
                }
                console.log("ok")
            },
            fail: function () {
                alert("Disconnect!");
            },
        });
    });
});

function delNrows() {
        var selection = tablex.getSelected();
        var col = selection[0][1];
        for(i = 0;i < datax.length;i++){
            if(datax[i][col] === ""){
                datax.splice(i,1);
                i--;
            }
        }
        refreshTable(datax);
    }
function refreshcolunms() {
    var iobj = document.getElementById("srhbykey-b");
    iobj.innerHTML ="Colunms<span class=\"caret\"></span>";
    var srhkey_u = document.getElementById("srhbykey-u");
    srhkey_u.innerHTML = "";
    for(var col in datax[0])
    {
        var li = document.createElement("li");
        li.setAttribute("class","minkey");
        li.setAttribute("id",datax[0][col]);
        li.innerHTML ="<a href=\"#\">" + datax[0][col] + "</a>";
        srhkey_u.appendChild(li);
    }
    $(".minkey").click(function () {
            var bobj = document.getElementById("srhbykey-b");
            bobj.innerHTML = this.id + "<span class=\"caret\"></span>";
    });
}
function srhbykey() {
    var srhkey = document.getElementById("srhbykey-b");
    if(srhkey.value === "1")
    {
        addlength(1,"srhbykey-b");
        Init2();
        srhkey.value = "0";
    }
    else {
         addlength(-1,"srhbykey-b");
        Init2();
        srhkey.value = "1";
    }
     $("#srhbykey-d").slideToggle("fast");
}

function inittable() {
    var datac = [
            [""],
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
                 "about1":{
                     name:'Delete Null Rows',
                     callback: function(){
                         setTimeout(delNrows(),0);
                     }
                 },
                 "about2":{
                     name:'Filter by Keywords',
                     callback: function () {
                         setTimeout(srhbykey(),0);
                     }
                 },
             },
         },
    });
     tablex = table;
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
        width: 0.6*window.innerWidth,
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
    });
    tablex = table;
}
function reversedata(data) {
    var keys = new Array();
    for(var key in data){
        keys.push(key);
    }
    var datac = new Array();
    for( k = 0,klen = data[keys[0]].length+1;k<klen;k++)
        datac[k] = new Array();
    datac[0] = keys;
    for(j = 0,len=keys.length; j < len; j++)
        for(i = 1,ilen = data[keys[0]].length+1;i < ilen;i++)
            datac[i].push(data[keys[j]][i]);
    return datac;
}