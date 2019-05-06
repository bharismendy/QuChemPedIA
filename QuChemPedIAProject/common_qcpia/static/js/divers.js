function html_converter() {
    var doc = new jsPDF();
    var html=window.document.getElementsByTagName("body")[0];
    alert (html);
    doc.fromHTML(html , 15, 15, {
        'width': 800
    });

    setTimeout(function(){
        doc.save('molecular_export');
    },2000);
}