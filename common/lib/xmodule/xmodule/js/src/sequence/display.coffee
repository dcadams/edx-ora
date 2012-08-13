class @Sequence
  constructor: (element) ->
    @el = $(element).find('.sequence')
    @contents = @$('.seq_contents')
    @id = @el.data('id')
    @initProgress()
    @bind()
    @render parseInt(@el.data('position'))

  $: (selector) ->
    $(selector, @el)

  bind: ->
    @$('#sequence-list a').click @goto

  initProgress: ->
    @progressTable = {}  # "#problem_#{id}" -> progress


  hookUpProgressEvent: ->
    $('.problems-wrapper').bind 'progressChanged', @updateProgress

  mergeProgress: (p1, p2) ->
    # if either is "NA", return the other one
    if p1 == "NA"
      return p2
    if p2 == "NA"
      return p1

    # Both real progresses
    if p1 == "done" and p2 == "done"
      return "done"

    # not done, so if any progress on either, in_progress
    w1 = p1 == "done" or p1 == "in_progress"
    w2 = p2 == "done" or p2 == "in_progress"
    if w1 or w2
      return "in_progress"

    return "none"

  updateProgress: =>
    new_progress = "NA"
    _this = this
    $('.problems-wrapper').each (index) ->
      progress = $(this).attr 'progress'
      new_progress = _this.mergeProgress progress, new_progress

    @progressTable[@position] = new_progress
    @setProgress(new_progress, @link_for(@position))

  setProgress: (progress, element) ->
      # If progress is "NA", don't add any css class
      element.removeClass('progress-none')
             .removeClass('progress-some')
             .removeClass('progress-done')
      switch progress
        when 'none' then element.addClass('progress-none')
        when 'in_progress' then element.addClass('progress-some')
        when 'done' then element.addClass('progress-done')

  toggleArrows: =>
    @$('.sequence-nav-buttons a').unbind('click')

    if @position == 1
      @$('.sequence-nav-buttons .prev a').addClass('disabled')
    else
      @$('.sequence-nav-buttons .prev a').removeClass('disabled').click(@previous)

    if @position == @contents.length
      @$('.sequence-nav-buttons .next a').addClass('disabled')
    else
      @$('.sequence-nav-buttons .next a').removeClass('disabled').click(@next)

  render: (new_position) ->
    if @position != new_position
      if @position != undefined
        @mark_visited @position
        $.postWithPrefix "/modx/#{@id}/goto_position", position: new_position

      @mark_active new_position
      @$('#seq_content').html @contents.eq(new_position - 1).text()
      XModule.loadModules('display', @$('#seq_content'))

      MathJax.Hub.Queue(["Typeset", MathJax.Hub])
      @position = new_position
      @toggleArrows()
      @hookUpProgressEvent()

  goto: (event) =>
    event.preventDefault()
    new_position = $(event.target).data('element')
    Logger.log "seq_goto", old: @position, new: new_position, id: @id

    # On Sequence chage, destroy any existing polling thread 
    #   for queued submissions, see ../capa/display.coffee
    if window.queuePollerID
      window.clearTimeout(window.queuePollerID)
      delete window.queuePollerID

    @render new_position

  next: (event) =>
    event.preventDefault()
    new_position = @position + 1
    Logger.log "seq_next", old: @position, new: new_position, id: @id
    @render new_position

  previous: (event) =>
    event.preventDefault()
    new_position = @position - 1
    Logger.log "seq_prev", old: @position, new: new_position, id: @id
    @render new_position

  link_for: (position) ->
    @$("#sequence-list a[data-element=#{position}]")

  mark_visited: (position) ->
    # Don't overwrite class attribute to avoid changing Progress class
    element = @link_for(position)
    element.removeClass("inactive")
    .removeClass("active")
    .addClass("visited")

  mark_active: (position) ->
    # Don't overwrite class attribute to avoid changing Progress class
    element = @link_for(position)
    element.removeClass("inactive")
    .removeClass("visited")
    .addClass("active")