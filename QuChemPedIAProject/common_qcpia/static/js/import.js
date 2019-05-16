function ask_job_type(csrftoken) {
    /**
     * ask the user what is the job_type of he's calculation
     **/
    var csrftoken = getCookie('csrftoken');
    //select the main div
    var form_import_html = document.getElementById("form_import_div");

    //adding the instruction of what to do
    var form_instruction = document.createElement("P");
    form_instruction.innerText = "choose your the job type (optionnal) :";
    form_import_html.appendChild(form_instruction);

    //adding csrf_token
    var form_csrf_token = document.createElement("INPUT");
    form_csrf_token.setAttribute('type','hidden');
    form_csrf_token.setAttribute('name','csrfmiddlewaretoken');
    form_csrf_token.setAttribute('value', csrftoken);

    // adding form csrf token (cross site requ"est forgery)
    form_import_html.appendChild(form_csrf_token);

    //adding the OPT options
    var job_type_opt_div = document.createElement("DIV");
    job_type_opt_div.setAttribute('class','form-check-inline');

    var job_type_opt_label = document.createElement("LABEL");
    job_type_opt_label.setAttribute('class','form-check-label');
    job_type_opt_label.setAttribute('title','Ground state geometry optimization');
    job_type_opt_label.innerHTML +="&nbsp;OPT&nbsp;";

    var job_type_opt_input = document.createElement("INPUT");
    job_type_opt_input.setAttribute('type','checkbox');
    job_type_opt_input.setAttribute('name','job_type_opt');
    job_type_opt_input.setAttribute('value','OPT');
    job_type_opt_input.setAttribute('id','OPT');
    job_type_opt_input.setAttribute('onchange','uncheck_job_type_none()');
    job_type_opt_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_opt_div.appendChild(job_type_opt_label);
    job_type_opt_label.appendChild(job_type_opt_input);

    //adding the FREQ options
    var job_type_freq_div = document.createElement("DIV");
    job_type_freq_div.setAttribute('class','form-check-inline');

    var job_type_freq_label = document.createElement("LABEL");
    job_type_freq_label.setAttribute('class','form-check-label');
    job_type_freq_label.setAttribute('title','Normal modes');
    job_type_freq_label.innerHTML +="&nbsp;FREQ&nbsp;";

    var job_type_freq_input = document.createElement("INPUT");
    job_type_freq_input.setAttribute('type','checkbox');
    job_type_freq_input.setAttribute('name','job_type_freq');
    job_type_freq_input.setAttribute('value','FREQ');
    job_type_freq_input.setAttribute('onchange','uncheck_job_type_none()');
    job_type_freq_input.setAttribute('id','FREQ');
    job_type_freq_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_freq_div.appendChild(job_type_freq_label);
    job_type_freq_label.appendChild(job_type_freq_input);

    //adding the SP options
    var job_type_sp_div = document.createElement("DIV");
    job_type_sp_div.setAttribute('class','form-check-inline');

    var job_type_sp_label = document.createElement("LABEL");
    job_type_sp_label.setAttribute('class','form-check-label');
    job_type_sp_label.setAttribute('title','Single point energy');
    job_type_sp_label.innerHTML +="&nbsp;SP-/+&nbsp;";

    var job_type_sp_input = document.createElement("INPUT");
    job_type_sp_input.setAttribute('type','checkbox');
    job_type_sp_input.setAttribute('name','job_type_sp');
    job_type_sp_input.setAttribute('value','SP');
    job_type_sp_input.setAttribute('onchange','uncheck_job_type_none()');
    job_type_sp_input.setAttribute('id','SP');
    job_type_sp_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_sp_div.appendChild(job_type_sp_label);
    job_type_sp_label.appendChild(job_type_sp_input);

    //adding the TD options
    var job_type_td_div = document.createElement("DIV");
    job_type_td_div.setAttribute('class','form-check-inline');

    var job_type_td_label = document.createElement("LABEL");
    job_type_td_label.setAttribute('class','form-check-label');
    job_type_td_label.setAttribute('title','Excited states energies');
    job_type_td_label.innerHTML +="&nbsp;TD&nbsp;";

    var job_type_td_input = document.createElement("INPUT");
    job_type_td_input.setAttribute('type','checkbox');
    job_type_td_input.setAttribute('name','job_type_td');
    job_type_td_input.setAttribute('value','TD');
    job_type_td_input.setAttribute('id','TD');
    job_type_td_input.setAttribute('onchange','uncheck_job_type_none()');
    job_type_td_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_td_div.appendChild(job_type_td_label);
    job_type_td_label.appendChild(job_type_td_input);

    //adding the OPT_ES/ET options
    var job_type_opt_es_et_div = document.createElement("DIV");
    job_type_opt_es_et_div.setAttribute('class','form-check-inline');

    var job_type_opt_es_et_label = document.createElement("LABEL");
    job_type_opt_es_et_label.setAttribute('class','form-check-label');
    job_type_opt_es_et_label.setAttribute('title','Excited state geometry optimization');
    job_type_opt_es_et_label.innerHTML +="&nbsp;OPT_ES/ET&nbsp;";

    var job_type_opt_es_et_input = document.createElement("INPUT");
    job_type_opt_es_et_input.setAttribute('type','checkbox');
    job_type_opt_es_et_input.setAttribute('name','job_type_opt_es_et');
    job_type_opt_es_et_input.setAttribute('value','OPT_ES_ET');
    job_type_opt_es_et_input.setAttribute('id','OPT_ES_ET');
    job_type_opt_es_et_input.setAttribute('onchange','uncheck_job_type_none()');
    job_type_opt_es_et_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_opt_es_et_div.appendChild(job_type_opt_es_et_label);
    job_type_opt_es_et_label.appendChild(job_type_opt_es_et_input);

    //adding the FREQ_ES/ET options
    var job_type_freq_es_et_div = document.createElement("DIV");
    job_type_freq_es_et_div.setAttribute('class','form-check-inline');

    var job_type_freq_es_et_label = document.createElement("LABEL");
    job_type_freq_es_et_label.setAttribute('class','form-check-label');
    job_type_freq_es_et_label.innerHTML +="&nbsp;FREQ_ES/ET&nbsp;";

    var job_type_freq_es_et_input = document.createElement("INPUT");
    job_type_freq_es_et_input.setAttribute('type','checkbox');
    job_type_freq_es_et_input.setAttribute('name','job_type_freq_es_et');
    job_type_freq_es_et_input.setAttribute('value','FREQ_ES_ET');
    job_type_freq_es_et_input.setAttribute('id','FREQ_ES_ET');
    job_type_freq_es_et_input.setAttribute('onchange','uncheck_job_type_none()');
    job_type_freq_es_et_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_freq_es_et_div.appendChild(job_type_freq_es_et_label);
    job_type_freq_es_et_label.appendChild(job_type_freq_es_et_input);

    //adding the dont know options
    var job_type_none_div = document.createElement("DIV");
    job_type_none_div.setAttribute('class','form-check-inline');

    var job_type_none_label = document.createElement("LABEL");
    job_type_none_label.setAttribute('class','form-check-label');
    job_type_none_label.innerHTML +="&nbsp;I don't know&nbsp;/&nbsp;Other&nbsp;";

    var job_type_none_input = document.createElement("INPUT");
    job_type_none_input.setAttribute('type','checkbox');
    job_type_none_input.setAttribute('name','job_type_none');
    job_type_none_input.setAttribute('value','none');
    job_type_none_input.setAttribute('id','none');
    job_type_none_input.setAttribute('onchange','uncheck_all()');
    job_type_none_input.setAttribute('class','form-check-input');

    // add element to the form
    job_type_none_div.appendChild(job_type_none_label);
    job_type_none_label.appendChild(job_type_none_input);

    // adding all element to the form
    form_import_html.appendChild(job_type_opt_div);
    form_import_html.appendChild(job_type_freq_div);
    form_import_html.appendChild(job_type_sp_div);
    form_import_html.appendChild(job_type_td_div);
    form_import_html.appendChild(job_type_opt_es_et_div);
    form_import_html.appendChild(job_type_freq_es_et_div);
    form_import_html.appendChild(job_type_none_div);

    var button_send = document.createElement("BUTTON");
    button_send.setAttribute("class","btn btn-primary");
    button_send.setAttribute("type","submit");
    button_send.setAttribute("id","btn_upload");
    button_send.setAttribute("name","btn_upload");
    button_send.innerText = "Send";

    form_import_html.appendChild(button_send);
}

function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    var files = evt.dataTransfer.files;
    // files is a FileList of File objects. List some properties.
    document.getElementById('fileInput').files = evt.dataTransfer.files;
    var test_job_ask_exist = document.getElementById("btn_upload");
    if (test_job_ask_exist === null)
    {
        ask_job_type();
    }
    evt.preventDefault();
}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}
function display_job_type() {
    var test_job_ask_exist = document.getElementById("btn_upload");
    if (test_job_ask_exist === null)
    {
        ask_job_type();
    }
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function uncheck_all(){
    var checks = document.querySelectorAll('#' + 'form_import_div' + ' input[type="checkbox"]');
    for(var i =0; i< checks.length;i++){
        var check = checks[i];
        if(!check.disabled && !(check.name === "job_type_none")){
            check.checked = false;
        }
    }
}
function uncheck_job_type_none() {
    document.getElementById('none').checked = false
}

function myDropzoneJs(){
     Dropzone.autoDiscover = false;
     Dropzone.options.myAwesomeDropzone = {
         url:"{% url 'dashboard/import' %}",
         maxFilesize: 5000,
         addRemoveLinks : true,
         dictDefaultMessage: "Drop your log files here or click to upload",
         dictResponseError: 'Error uploading file!',
         autoQueue:false,
         autoProcessQueue:true,
         maxFiles: 1,
         success: function (file, response) {
             alert('success!');
             location.reload();
             this.removeFile(file); //todo discuter de quoi faire
         },
         error: function (file, response) {
             alert('fail!');
             },
         init: function () {
             var myDropzone = this;
             // Update selector to match your button
             $("#button").click(function (e) {
                 alert('success!');
                 e.preventDefault();
                 myDropzone.processQueue();
             });
         }
     };
}
