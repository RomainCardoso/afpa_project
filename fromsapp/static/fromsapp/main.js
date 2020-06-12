$(document).ready(function() {
  $('#search_button').click(function() {
    if($('#id_item').val() != '') {
      $(this).hide()
      $('#load_button').show()
    }
  });
});
