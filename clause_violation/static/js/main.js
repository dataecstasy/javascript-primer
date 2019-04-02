//
//$(document).ready(function() {
//
//	$("#loader").css("display", "none");
//});


$('.dropdown-menu input[type="checkbox"]').on('click', function() {
 
 var title = $(this).closest('.dropdown-menu').find('input[type="checkbox"]').val(),
    title = $(this).val() + ",";
  if ($(this).is(':checked')) {
	var str = $('#btntxt').text();
	var res = str.replace("Please Select Value", "");
	$('#btntxt').text(res);
    $('.multiSel').append(title);
    $(".hida").hide();
  } else {
	$('#btntxt').text("Please select Value");
  }
  
});
//Program a custom submit function for the form
$("form#data").submit(function(event){
event.preventDefault();
$("#loader").css("display", "block");
 move();
  //grab all form data  
  var formData = new FormData($(this)[0]);

  $.ajax({
    url: 'http://127.0.0.1:5000/router',
    type: 'POST',
    data: formData,
    async: false,
    cache: false,
    contentType: false,
    processData: false,
    success: function (returndata) {

//		alert(returndata);
	  var obj = $.parseJSON(returndata)
//		alert(obj['Start_End']);
      $("#outputBox").show();
      $(".outputText").text(obj['Start_End']);
      $(".feedbackText").text(obj['Response']);
      $(".reason").text(obj['Reason']);
      $(".gap").text(obj['Gap_outcome']);

//	  setTimeout(function() {
//    $("#loader").css("display", "none");
//	}, 4000);
}
  });
 
  return false;
});
//$("#loader").unbind('click').bind('click',  function (e)
//{
////    alert('hi')
//	$("#loader").css("display", "block");
//
//});

function move() {
    var elem = document.getElementById("myBar"); 
    var width = 1;
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++; 
            elem.style.width = width + '%'; 
        }
    }
}