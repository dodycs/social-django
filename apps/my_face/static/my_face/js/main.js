$(document).ready(function () {
   $("#myModal").modal('show');
   setTimeout(function () {
      $('#myModal').modal('hide');
   }, 1200);
});