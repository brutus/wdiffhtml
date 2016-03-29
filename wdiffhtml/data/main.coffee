toggle = (event) ->
  obj = $(this)
  if obj.attr('id') == 'navcontroll'
    $('article').toggleClass('topspace')
  $('span', obj).toggleClass('hidden')
  target = obj.attr('data-target')
  tclass = obj.attr('data-class')
  $(target).toggleClass(tclass)
  return false


$ ->
  $('button').on('click', toggle)
  $('#navcontroll').toggleClass('hidden')
