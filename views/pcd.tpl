
%helper = app.helper
%rebase layout globals(), title='Wall view', js=[ 'pcd/js/pcd.js'], refresh=True, user=user, print_menu=False, print_header=True, menu_part='/pcd'

<h1>jQuery Example</h1>
<p>
  <input type="text" size="5" name="a"> +
  <input type="text" size="5" name="b"> =
  <span id="result">?</span>
<p><a href=# id="calculate">calculate server side</a>

