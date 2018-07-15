var index = new Array();
$(document).ready(function () {
    $(".minop").click(function () {
        console.log(index);
        if(this.value == "0")
        {
            index.push(this.id);
            console.log(index);
            this.value = "1";
            console.log(this.firstChild);
            var a1 = this.firstChild;
            a1.innerHTML += "<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>";
        }
        else
        {
            this.value = "0";
            var a2 = this.firstChild;
            a2.innerHTML = a2.innerText;
            var i = index.indexOf(this.id);
            index.splice(i,1);
            console.log(index);
        }
        $.ajax({
           type: "post",
           url: "/Drug/ProjectionResult/",
           data:{
               'index_of_drug': index,
           },
            success:function(data){
                refreshTable(data);
            },
            fail: function () {
                alert("Disconnect!");
            },
        });
    });
});