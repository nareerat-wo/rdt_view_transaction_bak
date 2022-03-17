var g_entity_group_json = {};
var g_entity_name_json = {};
var g_frequency_json = {};
var g_criteria_json = {};
var g_classification_json = {};
var g_view_tx_result_json = {};
var g_bot_abbr = '';
var g_bot_abbr_mod = '';
var g_product = '';
var g_obj = {}
var g_check_status = true;
$(document).ready(function(){

   $('.main-menu a[href="#menu1-tab"]').tab('show')
   $('#btn-criteria').hide();

   // console.log(entity_group_dic);

   entity_group_dic = entity_group_dic.replace(/&quot;/g, '"');
   g_entity_group_json = JSON.parse(entity_group_dic.toString());

   entity_name_dic = entity_name_dic.replace(/&quot;/g, '"');
   g_entity_name_json = JSON.parse(entity_name_dic.toString());

   frequency_dic = frequency_dic.replace(/&quot;/g, '"');
   g_frequency_json = JSON.parse(frequency_dic.toString());

   criteria_dic = criteria_dic.replace(/&quot;/g, '"');
   g_criteria_json = JSON.parse(criteria_dic.toString());

   classification_dic = classification_dic.replace(/&quot;/g, '"');
   g_classification_json = JSON.parse(classification_dic.toString());

   view_tx_result_dic = view_tx_result_dic.replace(/&quot;/g, '"');
   g_view_tx_result_json = JSON.parse(view_tx_result_dic.toString());

   $('#content-view-data-entity').hide();

   // console.log(g_frequency_json);

   setEntityGroup();
   setEntityName();
});

// function search_removeDefault() {
//    $('#search_form option[value=""],option:not([value])').remove();
// }

function setEntityGroup(){
   $("#data-entity-group").empty();
   for(let i=0;i<g_entity_group_json['Data_Entity_Group'].length;i++){
      $("#data-entity-group").append('<option value="' + g_entity_group_json['Data_Entity_Group'][i] + '">' + g_entity_group_json['Data_Entity_Group'][i] + '</option>')
   }
}

function setEntityName(){
   $("#data-entity-name").empty();
   for(let i=0;i<g_entity_name_json['Data_Entity_Name'].length;i++){
      if(g_entity_name_json['Data_Entity_Group'][i] == $("#data-entity-group option:selected").text()){
         $("#data-entity-name").append('<option value="' + g_entity_name_json['BOT_ABBR'][i] + '">' + g_entity_name_json['Data_Entity_Name'][i] + '(' + g_entity_name_json['BOT_ABBR'][i] + ')' + '</option>');
      }
   }
}

function setFrequency(){
   $("#criteriaSelect1").empty();
   g_bot_abbr = $("#data-entity-name option:selected").text()
   g_bot_abbr_mod = g_bot_abbr.split('(');
   g_bot_abbr_mod = g_bot_abbr_mod[1].replace(')', '');
   for(let i=0;i<g_frequency_json['Frequency'].length;i++){
      if(g_bot_abbr_mod == g_frequency_json['BOT_ABBR'][i]){
         $("#criteriaSelect1").append('<option value="' + g_frequency_json['Frequency'][i] + '">' + g_frequency_json['Frequency'][i] + '</option>')
      }
   }
}

function LastDayOfMonth(Year, Month){
   return(new Date((new Date(Year, Month+1,1))-1)).getDate();
}

function setDatepicker(){
   let optionSelected = $("#criteriaSelect1 option:selected").text();
   if(optionSelected == 'Monthly'){
      $('#datepickers').val('');
      $('#datepickers').datepicker("destroy");
      $('#datepickers').datepicker({ 
      uiLibrary: 'bootstrap4', 
      format: 'yyyy-mm-dd', 
      iconsLibrary: 'fontawesome', 
      size: 'small',
      disableDates: function (date){
         if (date.getDate() == LastDayOfMonth(date.getFullYear(),date.getMonth())) {
            return true;
         } 
         else {
            return false;
         }
      }});
   }
   else{
      $('#datepickers').val('');
      $('#datepickers').datepicker("destroy");
      $('#datepickers').datepicker({
         uiLibrary: 'bootstrap4',
         format: 'yyyy-mm-dd',
         iconsLibrary: 'fontawesome',
         size: 'small' });
   }
   // $('#datepickers').datepicker('disabled');
   $('#datepickers').attr('readonly','readonly');
}

function setDatepickerFromObj(datepickerID){
   let datepickerIDCombime = '#' + datepickerID
   $(datepickerIDCombime).datepicker({ uiLibrary: 'bootstrap4', format: 'yyyy-mm-dd', iconsLibrary: 'fontawesome', size: 'small' });
}

function setMultipleSelect(classificationID){
   $(classificationID).attr('multiple', '');
                  
   $(classificationID).selectpicker('refresh');
}

function search_removeDefault() {
   $('.multiple-select option[value=""],option:not([value])').remove();
}

function createCriteriaSections(g_bot_abbr_mod){
   let require = '';
   let id = 1;
   let form_length = 2;
   let div_id = '#criteria' + id.toString();
   // console.log(div_id);
   $('#search-criteria').empty();
   $('#search-criteria').append('<div class="form-row" id=' + '"criteria' + id.toString() + '"' + '>')
   $(div_id).append('<div class="col"><div class="form-group"><label for="criteriaSelect1">Frequency<span style="color: red">*</span> </label><select class="form-control form-control-sm" id="criteriaSelect1"><option value="daily">Daily</option></select></div></div></div>');
   $(div_id).append('<div class="col"><div class="form-group"><label for="data-entity-group">Data Date<span style="color: red">*</span> </label><input id="datepickers" readonly="readonly" class="form-control form-control-sm"  /></div></div></div>');
   for(let i=0;i<g_criteria_json['elm_name'].length;i++){
      // console.log(div_id);
      if(g_criteria_json['BOT_ABBR'][i].toLowerCase() == g_bot_abbr_mod.toLowerCase()){
         // console.log(g_criteria_json['elm_name'][i]);
         form_length += 1;
         // console.log(form_length);
         if (form_length > 5) {
            form_length = 1;
            id += 1;
            div_id = '#criteria' + id.toString();
            $('#search-criteria').append('<div class="form-row" id=' + '"criteria' + id.toString() + '"' + '>')
         }
         if(g_criteria_json['elm_type'][i] == 'date'){
            if(g_criteria_json['criteria_require_flag'][i] == 'Y'){
               require = '*';
            }
            else{
               require = '';
            }
            $(div_id).append('<div class="col"><div class="form-group"><label for=' + g_criteria_json['elm_name'][i] + '_label' + '>' + g_criteria_json['elm_desc'][i] + '<span style="color: red">' + require + '</span>' + '</label><input id=' +  g_criteria_json['elm_name'][i] + ' class="form-control form-control-sm"  /></div></div></div>');
            if(!require){
               $('#'+g_criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
            }
            setDatepickerFromObj(g_criteria_json['elm_name'][i]);
         }
         else if(g_criteria_json['elm_type'][i] == 'string'){
            if(g_criteria_json['criteria_require_flag'][i] == 'Y'){
               require = '*';
            }
            else{
               require = '';
            }
            $(div_id).append('<div class="col"><div class="form-group"><label for=' + g_criteria_json['elm_name'][i] + '_label' + '>' + g_criteria_json['elm_desc'][i] + '<span style="color: red">' + require + '</span>' +'</label><input id=' +  g_criteria_json['elm_name'][i] + ' class="form-control form-control-sm" type="text"  /></div></div></div>');
            if(!require){
               $('#'+g_criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
            }
         }
         else if(g_criteria_json['elm_type'][i] == 'classification'){
            if(g_criteria_json['criteria_require_flag'][i] == 'Y'){
               require = '*';
            }
            else{
               require = '';
            }

            $(div_id).append('<div class="col"><div class="form-group"><label for=' + g_criteria_json['elm_name'][i] + '_label' + '>' + g_criteria_json['elm_desc'][i] + '<span style="color: red">' + require + '</span>' + '</label><select class="form-control form-control-sm multiple-select" title="---Please Select---" onchange="search_removeDefault()" id=' + g_criteria_json['elm_name'][i] +'>' + '</select></div></div></div>');
            $("#" + g_criteria_json['elm_name'][i]).append('<option value title hidden></option>');
            // $("#" + g_criteria_json['elm_name'][i]).append('<option value="none" selected disabled hidden>Select an Option</option>')
            if(!require){
               $('#'+g_criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
            }
            for(let j=0;j<g_classification_json['param_nm'].length;j++){
               if(g_classification_json['param_nm'][j] == g_criteria_json['classification'][i]){
                  $("#" + g_criteria_json['elm_name'][i]).append('<option value="' + g_classification_json['param_cd'][j] + '">' + g_classification_json['param_cd'][j] + ' ' + g_classification_json['param_val'][j] + '</option>');
               }
            }
            setMultipleSelect("#" + g_criteria_json['elm_name'][i]);
         }
      }
   }
   // $(".multiple-select").on('change', function() {
   //    alert( this.value );
   // });
   $('#search-criteria').append('<div><button id="btn-criteria" class="btn btn-sm float-right" type="button"><i class="fas fa-filter"></i> Apply</button></div>');
   
   $("#btn-criteria").click(function(){
      let model_abbr = '';
      let current_bot_abbr = $("#data-entity-name option:selected").text();
      let current_bot_abbr_mod = current_bot_abbr.split('(');
      current_bot_abbr_mod = current_bot_abbr_mod[1].replace(')', '');
      frequency_text = $("#criteriaSelect1 option:selected").text()
      if(current_bot_abbr_mod == g_bot_abbr_mod){
         if(validateFields()){
            model_abbr = getModelAbbr(current_bot_abbr_mod, frequency_text);
            // var today = new Date();
            // var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
            // var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            // var dateTime = date+' '+time;
            let time_stamp = setDateTime();
            $('#content-view-data-entity').show();
            checkInitDatatable();
            setValidationStatus(model_abbr, time_stamp, current_bot_abbr_mod);
         }
      }
      else{
         bootbox.alert({
            message: 'Current Data Entity Name (' + current_bot_abbr_mod + ') ' + 'does not match with Entity name (' + g_bot_abbr_mod + ')',
            centerVertical: true
         });
      }
   });
   $('#criteria1').change();

}

function validateFields(){
   if($('#datepickers').val() == ''){
      g_check_status = false;
      bootbox.alert({
         message: 'Please fill in Data Date',
         centerVertical: true
      });
   }
   else{
      g_check_status = true;
      g_obj['frequency'] = $('#criteriaSelect1').val()
      g_obj['bsns_dt'] = $('#datepickers').val();
      for(let i=0;i<g_criteria_json['elm_name'].length;i++){
         if(g_criteria_json['BOT_ABBR'][i].toLowerCase() == g_bot_abbr_mod.toLowerCase()){
            if(g_criteria_json['criteria_require_flag'][i] == 'Y'){
               if($('#'+g_criteria_json['elm_name'][i]).val() == ''){
                  bootbox.alert({
                     message: 'Please fill in ' + g_criteria_json['elm_name'][i],
                     centerVertical: true
                 });
                  g_check_status = false;
                  break;
               }
               else{
                  g_obj[g_criteria_json['elm_name'][i]] = $('#'+g_criteria_json['elm_name'][i]).val();
               }
            }
            else{
               g_obj[g_criteria_json['elm_name'][i]] = $('#'+g_criteria_json['elm_name'][i]).val();
            }
         }
      }
   }
   return g_check_status
}
function setTotalRecord(model_abbr, current_bot_abbr_mod){
   $.ajax({
      type: "POST",
      url: "getTotalRecord",
      data: {
         'entity_fields': JSON.stringify(g_obj),
         'bot_abbr': g_bot_abbr_mod,
         'model_abbr': model_abbr,
         'entity_group_sj': getEntityGroupSJ(current_bot_abbr_mod).replace(/\s/g, '')
      },
      datatype: 'json',
      beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
          // show image container
         // $("#loading").attr("style", "visibility: visible;");
      },
      complete: function (data) {
          // Hide image container
         // $("#loading").attr("style", "visibility: hidden;");
      },
      success: function (data) {
         let number_with_comma = ' ' + numberWithCommas(data) + ' ';
         // let str_record = number_with_comma.toString() + ' ' + 'records'
         let str_record = 'records';
         $("#total-records").text(number_with_comma);
         $('#total-records').css('color', '#565555');
         $('#total-records-s').text(str_record);
      },
      error: function (error) {
         bootbox.alert("Cannot set validation status.");
      }
  });
}

function setValidationStatus(model_abbr, time_stamp, current_bot_abbr_mod){
   $.ajax({
      type: "POST",
      url: "getValidationStatus",
      data: {
         'entity_fields': JSON.stringify(g_obj),
         'bot_abbr': g_bot_abbr_mod.toLowerCase(),
         'model_abbr': model_abbr,
      },
      datatype: 'json',
      beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
          // show image container
          $("#loading").attr("style", "visibility: visible;");
      },
      complete: function (data) {
          // Hide image container
          $("#loading").attr("style", "visibility: hidden;");
      },
      success: function (data) {
         $('#validation-status').text("");
         $('#date-v').text("");
         $("#total-records").text("");
         $("#total-records-s").text("");
         if(Object.entries(data).length === 0){
            $("#data-entity-tbl_wrapper").hide();
            $("#txt").show();
            $("#loading").attr("style", "visibility: hidden;");
         }
         else{
            $("#txt").hide();
            setTotalRecord(model_abbr, current_bot_abbr_mod);
            if(data['job_sts'] == 'SUCCESS' || data['job_sts'] == 'FAILED'){
               if(data['job_sts'] == 'SUCCESS'){
                  // $('#validation-status').text(data['job_sts'] + ' (' + data['entity_end_dttm'] + ')');
                  $('#validation-status').text(data['job_sts']);
                  $('#date-v').text(' (' + data['entity_end_dttm'] + ')')
                  $('#validation-status').css('color', 'green');
               }
               else if(data['job_sts'] == 'FAILED'){
                  // $('#validation-status').text(data['job_sts'] + ' (' + data['entity_end_dttm'] + ')');
                  $('#validation-status').text(data['job_sts']);
                  $('#date-v').text(' (' + data['entity_end_dttm'] + ')')
                  $('#validation-status').css('color', 'red');
               }
            }
            setElementNameList(model_abbr, time_stamp, current_bot_abbr_mod);
         }
      },
      error: function (error) {
         bootbox.alert("Cannot set validation status.");
      }
  });
}

function calculateTotalRecords(data){
   var num = data.length-2;
   var commas = num.toLocaleString("en-US");
   var commas = num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
   $('#total-records').text(commas)
}

function initDatatable(json_filter_by_bot_abbr, model_abbr, time_stamp, current_bot_abbr_mod){
   // console.log(json_filter_by_bot_abbr);
   column_arr = []
   column_def = []
   let key_value = '';
   let json_obj = {};

   for (let i=0;i<json_filter_by_bot_abbr.length;i++){
      // console.log('element name:'+json_filter_by_bot_abbr[i].entity_elm__elm_name);
      let data_col = { data: json_filter_by_bot_abbr[i].entity_elm__elm_name, orderable: false };
      column_arr.push(data_col);
   }
   for(let i=0;i<json_filter_by_bot_abbr.length;i++){
      if(json_filter_by_bot_abbr[i].visible_flag == 'N' && json_filter_by_bot_abbr[i].ajm_link_flag == 'N'){
         let json_col = { targets: i, visible: false, "createdCell": function (td, cellData, rowData, row, col) {json_obj[json_filter_by_bot_abbr[i].entity_elm__elm_name] = cellData}};
         column_def.push(json_col);
      }
      else if(json_filter_by_bot_abbr[i].visible_flag == 'Y' && json_filter_by_bot_abbr[i].ajm_link_flag == 'N'){
         // let json_col = {targets: i, visible: true, render: (data, type, row, meta) => {return `<div data-name="${json_filter_by_bot_abbr[i].entity_elm__elm_name}">${data}</div>`;}}
         let json_col = {targets: i, visible: true, "createdCell": function (td, cellData, rowData, row, col) {$(td).attr('data-name', json_filter_by_bot_abbr[i].entity_elm__elm_name);}}
         column_def.push(json_col);
      }
      else{
         let render = { targets: i, render: (data, type, row, meta) => {return `<a href="javascript: clickEditRow('${meta.row}', 'Adjust Data');">${data}</a>`;}, "createdCell": function (td, cellData, rowData, row, col) {$(td).attr("data-name", json_filter_by_bot_abbr[i].entity_elm__elm_name); $(td).attr("data-system", JSON.stringify(json_obj));}}
         column_def.push(render);
      }
   }
   
   // console.log(column_arr);
   // console.log(column_def);
   var table = $('#data-entity-tbl').DataTable({
      "serverSide": true,
      "processing": true,
      "searching": false,
      "bLengthChange": false,
      "bInfo": false,
      "pageLength": 20,
      "ajax": {
         type: "POST",
         url: "getDatafromCache",
         headers: { 'X-CSRFToken': CSRF_TOKEN },
         data: {
            'entity_fields': JSON.stringify(g_obj),
            'bot_abbr': g_bot_abbr_mod,
            'product': g_product,
            'model_abbr': model_abbr,
            'time_stamp': time_stamp,
            'entity_group_sj': getEntityGroupSJ(current_bot_abbr_mod).replace(/\s/g, '')
            // 'view_tx_result': JSON.stringify(json_filter_by_bot_abbr)
         },
      },
      // "data": dataset,

      "columnDefs": column_def,

      // "columnDefs": [
      // {
      //    "targets": 0,
      //    "checkboxes": {
      //       "selectRow": true,
      //       "searchable": false
      //    },
      // },
      // {
      //    "targets": 1,
      //    // "visible": false,
      //    'render': (data, type, row, meta) => {
      //       return  `<div data-before="${data}">${data}</div>`;
      //    }
      // },
      // {
      //    "targets": 2,
      //    "visible": false
      // }],
      "columns": column_arr,
      "bDestroy": true,
   });
   $("#data-entity-tbl_wrapper").addClass("ml-4");
   $("#data-entity-tbl>thead").addClass("thead-dark text-nowrap");
   $("#data-entity-tbl>tbody").addClass("text-nowrap width='100%'");

   for (var i=0;i<table.columns().nodes().length;i++) {
      table.columns(i).header().to$().text(json_filter_by_bot_abbr[i].entity_elm__elm_desc);
      table.columns(i).header().to$().attr('data-toggle', 'tooltip');
      table.columns(i).header().to$().attr('data-placement', 'top');
      table.columns(i).header().to$().attr('title', json_filter_by_bot_abbr[i].entity_elm__elm_desc_th);
   }
}

function getEntityGroupSJ(current_bot_abbr_mod){
   for(let i=0;i<g_frequency_json['entity_group_sj'].length;i++){
      if(g_frequency_json['BOT_ABBR'][i] == current_bot_abbr_mod.toLowerCase()){
         return g_frequency_json['entity_group_sj'][i];
      }
   }
}

function setElementNameList(model_abbr, time_stamp, current_bot_abbr_mod){
   var json_filter_by_bot_abbr = g_view_tx_result_json.filter(element => element.entity_elm__BOT_ABBR == current_bot_abbr_mod.toLowerCase());
   initDatatable(json_filter_by_bot_abbr, model_abbr, time_stamp, current_bot_abbr_mod);
}

function checkInitDatatable(){
   if ( $.fn.DataTable.isDataTable( '#data-entity-tbl' ) ) {
      var table = $("#data-entity-tbl").DataTable();
      table.clear();
      table.destroy();
   }
}

function getModelAbbr(current_bot_abbr_mod, frequency_text){
   for(let i=0;i<g_frequency_json['MODEL_ABBR'].length;i++){
      if(g_frequency_json['BOT_ABBR'][i] == current_bot_abbr_mod && g_frequency_json['Frequency'][i] == frequency_text){
         return g_frequency_json['MODEL_ABBR'][i];
      }
   }
}

function setDateTime(){
   var currentdate = new Date();
   let month = '' + (currentdate.getMonth() + 1);
   let day = '' + currentdate.getDate();
   let year = '' + currentdate.getFullYear();
   if (month.length < 2) {
      month = '0' + month;
   }
   if (day.length < 2) {
      day = '0' + day;
   }
   let time_stamp = year + month + day + currentdate.getHours() + currentdate.getMinutes() + currentdate.getSeconds();
   return time_stamp
}

function numberWithCommas(x) {
   return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

$("#btn-search-entity").click(function(){
   $('#btn-criteria').show();
   g_bot_abbr = $("#data-entity-name option:selected").text();
   g_bot_abbr_mod = g_bot_abbr.split('(');
   g_bot_abbr_mod = g_bot_abbr_mod[1].replace(')', '');
   g_product = $("#product option:selected").text();
   createCriteriaSections(g_bot_abbr_mod);
   setFrequency();
   setDatepicker();
   $('#criteriaSelect1').on('change', function () {
      setDatepicker();
   });
   // $('#btn-criteria-div').show();
});

$("#data-entity-group").change(function(){
   setEntityName();
});

$("#rowClick > tr").click(function(){
   $(this).toggleClass("active");
});

function setCheckBox(){
   // var table = $('#example').DataTable();
   // table.clear().destroy();
   var table = $('#data-entity-tbl').DataTable({
      "language": {
          search: '<i class="fas fa-search"></i>',
          searchPlaceholder: 'Search'
      },
      "bInfo" : false,
      'columnDefs': [
         {
            'targets': 0,
            'checkboxes': {
               'selectRow': true
            }
         }
      ],
      'select': {
         'style': 'multi'
      },
      'order': [[1, 'asc']],
      "bDestroy": true
   });
   $("#data-entity-tbl_wrapper").addClass("ml-4");
   // table.destroy();
}

$("#data-entity-tbl").parent().css({"overflow":"auto"})

$('#datepicker').datepicker({
   uiLibrary: 'bootstrap4'
});