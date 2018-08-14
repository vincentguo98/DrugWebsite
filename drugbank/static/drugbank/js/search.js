// var index = new Array();
// var datax;
// $(document).ready(function () {
//     $(".minop").click(function () {
//         if (this.value == "0") {
//             index.push(this.id);
//             this.value = "1";
//             var a1 = this.firstChild;
//             a1.innerHTML += "<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>";
//         } else {
//             this.value = "0";
//             var a2 = this.firstChild;
//             a2.innerHTML = a2.innerText;
//             var i = index.indexOf(this.id);
//             index.splice(i, 1);
//         }
//         // drug = { "drugindex":index[0]}
//         $.ajax({
//             type: "post",
//             url: "/Drug/ProjectionResult/",
//             data: {
//                 "drug": JSON.stringify(index)
//             },
//             dataType: "json",
//             success: function (data) {
//                 datax = reversedata(data);
//                 refreshTable(datax);
//                 refreshcolunms();
//             },
//             fail: function () {
//                 alert("Disconnect!");
//             },
//         });
//     });
//     $(".dropdown-menu").on('click', function (e) {
//         e.stopPropagation();
//     });
//     $("#drugbank-drug-div").on("change", function () {
//         $("#drugbank-drug-div option").each(function () {
//             val = $(this).html();
//             if (val != "smile" && val != "inchi") {
//                 if ($(this).get(0).selected) {
//                     $("#drugbank-" + val + "-div").show();
//                 } else {
//                     $("#drugbank-" + val + "-div").hide();
//                 }
//             }
//         });
//     });
// });



