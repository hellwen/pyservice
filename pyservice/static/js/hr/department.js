$.getJSON("http://127.0.0.1:8080/api/department", function(data) {
    var table = [];

    $('#content').html('<table cellpadding="0" cellspacing="0" border="0" class="display" id="example"></table>');

    table.push('<thead><tr>');
    table.push('<th>Department</th>');
    table.push('<th>Parent Department</th>');
    table.push('</tr></thead>');
    table.push('<tbody>');
    $.each(data.objects, function(key, item) {
        table.push('<tr>');
        table.push('<td>' + item.dept_name + '</td>');
        if (item.parent instanceof Object) {
            table.push('<td>' + item.parent.dept_name + '</td>');
        } else {
            table.push('<td></td>');
        }
        table.push('</tr>');
    });
    table.push('</tbody>');

    $("#example").html(table.join(''))
    $('#example').tablesorter({
        usNumberFormat : false,
        sortReset      : true,
        sortRestart    : true
    });
});