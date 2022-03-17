var entity_group_json = {};
var entity_name_json = {};
var frequency_json = {};
var criteria_json = {};
var classification_json = {};
var bot_abbr = '';
var bot_abbr_mod = '';
var product = '';
var obj = {}
var arr = [];
var check_status = true;
$(document).ready(function(){

   $('.main-menu a[href="#menu1-tab"]').tab('show')
   // console.log($("#exampleSelect2 option:selected").text());

   entity_group_dic = entity_group_dic.replace(/&quot;/g, '"');
   entity_group_json = JSON.parse(entity_group_dic.toString());
   entity_name_dic = entity_name_dic.replace(/&quot;/g, '"');
   entity_name_json = JSON.parse(entity_name_dic.toString());
   frequency_dic = frequency_dic.replace(/&quot;/g, '"');
   frequency_json = JSON.parse(frequency_dic.toString());

   criteria_dic = criteria_dic.replace(/&quot;/g, '"');
   criteria_json = JSON.parse(criteria_dic.toString());

   classification_dic = classification_dic.replace(/&quot;/g, '"');
   classification_json = JSON.parse(classification_dic.toString());

   $('#content-view-data-entity').hide();
   // $('#btn-criteria-div').hide();

   // console.log(classification_json);

   setEntityGroup();
   setEntityName();
   // console.log(criteria_json);

});

function setEntityGroup(){
   $("#data-entity-group").empty();
   for(let i=0;i<entity_group_json['Data_Entity_Group'].length;i++){
      // console.log(data[i])
      $("#data-entity-group").append('<option value="' + entity_group_json['Data_Entity_Group'][i] + '">' + entity_group_json['Data_Entity_Group'][i] + '</option>')
   }
   // $.ajax({
   //    type: "POST",
   //    url: "get_entity_group",
   //    datatype: 'json',
   //    beforeSend: function (xhr) {
   //        xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
   //        // show image container
   //        $("#loadingDataEntityGroup").attr("style", "visibility: visible;");
   //    },
   //    complete: function (data) {
   //        // Hide image container
   //        $("#loadingDataEntityGroup").attr("style", "visibility: hidden;");
   //    },
   //    success: function (data) {
   //       // console.log(data)
   //       for(let i=0;i<data.length;i++){
   //          // console.log(data[i])
   //          $("#exampleSelect1").append('<option value="' + data[i] + '">' + data[i] + '</option>')
   //       }
   //        //when ajax is running correctly
          
   //    },
   //    error: function (error) {
   //        alert("Somthing went wrong!!");
   //    }
   // });
}

function setEntityName(){
   $("#data-entity-name").empty();
   for(let i=0;i<entity_name_json['Data_Entity_Name'].length;i++){
      if(entity_name_json['Data_Entity_Group'][i] == $("#data-entity-group option:selected").text()){
         $("#data-entity-name").append('<option value="' + entity_name_json['BOT_ABBR'][i] + '">' + entity_name_json['Data_Entity_Name'][i] + '(' + entity_name_json['BOT_ABBR'][i] + ')' + '</option>');
      }
   }
   // $.ajax({
   //    type: "POST",
   //    url: "get_entity_name",
   //    datatype: 'json',
   //    beforeSend: function (xhr) {
   //        xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
   //        // show image container
   //       //  $("#loadingView").attr("style", "visibility: visible;");
   //    },
   //    complete: function (data) {
   //        // Hide image container
   //       //  $("#loadingView").attr("style", "visibility: hidden;");
   //    },
   //    success: function (data) {
   //       console.log(data[0]['EntityName'])
   //       for(let i=0;i<data[0]['EntityName'].length;i++){
   //          $("#exampleSelect2").append('<option value="' + data[0]['BOT_ABBR'][i] + '">' + data[0]['EntityName'][i] + '</option>')
   //       }
   //        //when ajax is running correctly
          
   //    },
   //    error: function (error) {
   //       console.log(error);
   //       alert("Somthing went wrong!!");
   //    }
   // });
}

function setFrequency(){
   $("#criteriaSelect1").empty();
   bot_abbr = $("#data-entity-name option:selected").text()
   bot_abbr_mod = bot_abbr.split('(');
   bot_abbr_mod = bot_abbr_mod[1].replace(')', '');
   for(let i=0;i<frequency_json['Frequency'].length;i++){
      if(bot_abbr_mod == frequency_json['BOT_ABBR'][i]){
         $("#criteriaSelect1").append('<option value="' + frequency_json['Frequency'][i] + '">' + frequency_json['Frequency'][i] + '</option>')
      }
   }
}

function LastDayOfMonth(Year, Month){
   return(new Date((new Date(Year, Month+1,1))-1)).getDate();
}

function setDatepicker(){
   let optionSelected = $("#criteriaSelect1 option:selected").text();
   // console.log(optionSelected);
   if(optionSelected == 'Daily'){
      $('#datepickers').val('');
      $('#datepickers').datepicker("destroy");
      // $('.datepicker').datepicker({
      //    format: 'dd-mm-yyyy'
      // });
      $('#datepickers').datepicker({ uiLibrary: 'bootstrap4', format: 'dd-mm-yyyy', iconsLibrary: 'fontawesome', size: 'small' });
      // console.log('if');
   }
   else{
      $('#datepickers').val('');
      $('#datepickers').datepicker("destroy");
      $('#datepickers').datepicker({ 
      uiLibrary: 'bootstrap4', 
      format: 'dd-mm-yyyy', 
      iconsLibrary: 'fontawesome', 
      size: 'small',
      disableDates: function (date){
         // console.log('test:', LastDayOfMonth(date.getFullYear(),date.getMonth()));
         if (date.getDate() == LastDayOfMonth(date.getFullYear(),date.getMonth())) {
            return true;
         } 
         else {
            return false;
         }
      }});
      // console.log('else');
   }
}

function setDatepickerFromObj(datepickerID){
   let datepickerIDCombime = '#' + datepickerID
   $(datepickerIDCombime).datepicker({ uiLibrary: 'bootstrap4', format: 'dd-mm-yyyy', iconsLibrary: 'fontawesome', size: 'small' });
}

function setMultipleSelect(classificationID){
   $(classificationID).attr('multiple', '');
                  
   $(classificationID).selectpicker('refresh');
}

function createCriteriaSections(bot_abbr_mod){
   let require = '';
   $("#criteria1").empty();
   $('#criteria1').append('<div class="form-group mr-3"><label for="criteriaSelect1">Frequency</label><select class="form-control form-control-sm" id="criteriaSelect1"><option value="daily">Daily</option></select></div></div>');
   // $('#criteria1').append('<div class="col"><div class="form-group"><label for="criteriaSelect1">Frequency</label><select class="form-control form-control-sm" id="criteriaSelect1"><option value="daily">Daily</option></select></div></div>');
   $('#criteria1').append('<div class="form-group mr-3"><label for="data-entity-group">Data Date</label><input id="datepickers" class="form-control form-control-sm"  /></div></div>');
   // bot_abbr = $("#exampleSelect2 option:selected").text()
   // bot_abbr_mod = bot_abbr.split('(');
   // bot_abbr_mod = bot_abbr_mod[1].replace(')', '');
   console.log(criteria_json);
   for(let i=0;i<criteria_json['elm_name'].length;i++){
      // bot_abbr = $("#exampleSelect2 option:selected").text()
      // console.log(bot_abbr_mod);
      // console.log(criteria_json['bot_abbr'][i]);
      // console.log(criteria_json['elm_name'][i])
      // console.log('bot_abbr_mod_lower_case: ' + bot_abbr_mod.toLowerCase());
      // console.log('criteria_json_bot_abbr_lower_case: ' + criteria_json['bot_abbr'][i].toLowerCase());
      if(criteria_json['bot_abbr'][i].toLowerCase() == bot_abbr_mod.toLowerCase()){
         // console.log(criteria_json['bot_abbr'][i]);
         if(criteria_json['elm_type'][i] == 'date'){
            // $('#criteria1').append('<div class="form-group mr-3"><label for=' + criteria_json['elm_name'][i] + '_label' + '>' + criteria_json['elm_desc'][i] + '</label><input id=' +  criteria_json['elm_name'][i] + ' class="form-control form-control-sm"  /></div></div>');
            if(criteria_json['criteria_require_flag'][i] == 'Y'){
               require = '*';
               // $('#'+criteria_json['elm_name'][i]).prop('required',true);
            }
            else{
               // $('#'+criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
               require = '';
            }
            $('#criteria1').append('<div class="form-group mr-3"><label for=' + criteria_json['elm_name'][i] + '_label' + '>' + criteria_json['elm_desc'][i] + '<span>' + require + '</span>' + '</label><input id=' +  criteria_json['elm_name'][i] + ' class="form-control form-control-sm"  /></div></div>');
            if(!require){
               $('#'+criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
            }
            setDatepickerFromObj(criteria_json['elm_name'][i]);
         }
         else if(criteria_json['elm_type'][i] == 'string'){
            // $('#criteria1').append('<div class="form-group mr-3"><label for=' + criteria_json['elm_name'][i] + '_label' + '>' + criteria_json['elm_desc'][i] + '</label><input id=' +  criteria_json['elm_name'][i] + ' class="form-control form-control-sm" type="text"  /></div></div>');
            // console.log('#'+criteria_json['elm_name'][i]);
            if(criteria_json['criteria_require_flag'][i] == 'Y'){
               require = '*';
               // $('#'+criteria_json['elm_name'][i]).attr('required',true);
            }
            else{
               // $('#'+criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
               require = '';
            }
            $('#criteria1').append('<div class="form-group mr-3"><label for=' + criteria_json['elm_name'][i] + '_label' + '>' + criteria_json['elm_desc'][i] + '<span>' + require + '</span>' +'</label><input id=' +  criteria_json['elm_name'][i] + ' class="form-control form-control-sm" type="text"  /></div></div>');
            if(!require){
               $('#'+criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
            }
         }
         else if(criteria_json['elm_type'][i] == 'classification'){
            // $('#criteria1').append('<div class="form-group mr-3 m-select"><label for=' + criteria_json['elm_name'][i] + '_label' + '>' + criteria_json['elm_desc'][i] + '</label><select class="form-control form-control-sm multiple-select" title="---Please Select---" id=' + criteria_json['elm_name'][i] + '>' + '</select></div></div>');
            // $("#" + criteria_json['elm_name'][i]).append('<option disabled class="text-hide" title hidden></option>')
            if(criteria_json['criteria_require_flag'][i] == 'Y'){
               require = '*';
               // $('#'+criteria_json['elm_name'][i]).attr('required',true);
            }
            else{
               // $('#'+criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
               require = '';
            }

            $('#criteria1').append('<div class="form-group mr-3 m-select"><label for=' + criteria_json['elm_name'][i] + '_label' + '>' + criteria_json['elm_desc'][i] + '<span style="color: red">' + require + '</span>' + '</label><select class="form-control form-control-sm multiple-select" title="---Please Select---" id=' + criteria_json['elm_name'][i] + '>' + '</select></div></div>');
            $("#" + criteria_json['elm_name'][i]).append('<option disabled class="text-hide" title hidden></option>')
            if(!require){
               $('#'+criteria_json['elm_name'][i]).attr("placeholder", "(Optional)");
            }
            for(let j=0;j<classification_json['param_nm'].length;j++){
               // console.log(classification_json['param_nm'][i] + " : " + criteria_json['classification'][i]);
               if(classification_json['param_nm'][j] == criteria_json['classification'][i]){
                  console.log(classification_json['param_nm'][j]);
                  $("#" + criteria_json['elm_name'][i]).append('<option value="' + classification_json['param_cd'][j] + '">' + classification_json['param_cd'][j] + ' ' + classification_json['param_val'][j] + '</option>');
               }
            }
            setMultipleSelect("#" + criteria_json['elm_name'][i]);
            // $('#'+criteria_json['elm_name'][i]).attr('multiple', '');
         }
      }
      // console.log(data[i])
      // $("#exampleSelect1").append('<option value="' + entity_group_json['Data_Entity_Group'][i] + '">' + entity_group_json['Data_Entity_Group'][i] + '</option>')
   }
   // $('#criteria1').append('<div id="btn-criteria-div" class="float-right"> <button id="btn-criteria" class="btn btn-sm float-right" type="button"><i class="fas fa-filter"></i> Apply</button></div>')
   $('#criteria1').change();
   // <select class="form-control form-control-sm" id="criteriaSelect2"><option value="monthly">Monthly</option></select>

}

// $('#criteriaSelect1').on('change', function(){
//    console.log("frequency_change");
//    // let optionSelected = $("#criteriaSelect1 option:selected", this).text();
//    setDatepicker();
// });

function validateFields(){
   if($('#datepickers').val() == ''){
      check_status = false;
      bootbox.alert({
         message: 'Please fill in Data Date',
         centerVertical: true
      });
   }
   else{
      // console.log('else');
      check_status = true;
      obj['frequency'] = $('#criteriaSelect1').val()
      obj['data_date'] = $('#datepickers').val();
      for(let i=0;i<criteria_json['elm_name'].length;i++){
         if(criteria_json['bot_abbr'][i] == bot_abbr_mod){
            // console.log('test null');
            if(criteria_json['criteria_require_flag'][i] == 'Y'){
               // console.log('test null');
               if($('#'+criteria_json['elm_name'][i]).val() == ''){
                  // console.log('test null');
                  // bootbox.alert('Please fill in ' + criteria_json['elm_name'][i]);
                  bootbox.alert({
                     message: 'Please fill in ' + criteria_json['elm_name'][i],
                     centerVertical: true
                 });
                  check_status = false;
                  break;
               }
               else{
                  obj[criteria_json['elm_name'][i]] = $('#'+criteria_json['elm_name'][i]).val();
               }
            }
            else{
               obj[criteria_json['elm_name'][i]] = $('#'+criteria_json['elm_name'][i]).val();
            }
            // console.log($('#'+criteria_json['elm_name'][i]).val());
            // obj[criteria_json['elm_name'][i]] = $('#'+criteria_json['elm_name'][i]).val();
         }
      }
   }
   console.log(obj)
   return check_status
}

function setValidationStatus(data){
   // console.log(data[data.length-1]['job_sts']);
   // console.log(data[data.length-1]['entity_end_dttm']);
   if(data[data.length-1]['job_sts'] == 'SUCCESS'){
      $('#validation-status').text(data[data.length-1]['job_sts'] + ' (' + data[data.length-1]['entity_end_dttm'] + ')');
      $('#validation-status').css('color', 'green');
   }
   else{
      $('#validation-status').text(data[data.length-1]['job_sts'] + ' (' + data[data.length-1]['entity_end_dttm'] + ')');
      $('#validation-status').css('color', 'red');
   }
}

function calculateTotalRecords(data){
   var num = data.length-2;
   var commas = num.toLocaleString("en-US");
   var commas = num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
   $('#total-records').text(commas)
   // console.log(data.length);
}

function getDescription(){
   $.ajax({
      type: "POST",
      url: "get_description",
      data: {
          'bot_abbr': bot_abbr_mod,
      },
      datatype: 'json',
      beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
          // show image container
         //  $('#content-view-data-entity').show();
         //  $("#loading").attr("style", "visibility: visible;");
      },
      complete: function (data) {
          // Hide image container
         //  $("#loading").attr("style", "visibility: hidden;");
      },
      success: function (data) {
         console.log(data);
         console.log(data['elm_desc'].length);
         // console.log(data['elm_desc'][0]);
         // console.log(criteria_json);
         // console.log(data[data.length-1]['job_sts']);
         // $("#data-entity-tbl").empty();
         // $("#data-entity-tbl>thead").empty();
         // $("#data-entity-tbl>tbody").empty();
         // $("#data-entity-tbl>thead").addClass("thead-dark text-nowrap");
         // $("#data-entity-tbl").append('<thead class="thead-dark text-nowrap"></thead>');
         // $("#data-entity-tbl").append('<tbody class="text-nowrap" width="100%"></tbody>');
         $("#data-entity-tbl>tr").hide();
         let table_head = '';
         let table_head_info = '';
         // table_head += '<tr><th></th>';
         // table_head_info += '<th>' + 'bsns_dt' + '</th>';
         table_head_info += '<th></th>';
         for(let i=0;i<data['elm_desc'].length;i++){
            table_head_info += '<th>' + data['elm_desc'][i] + '</th>';
            console.log(data['elm_desc'][i]);
            // console.log(data[data.length-2]['elm_desc'][i]);
         }

         table_head += table_head_info + '</tr>';
         // setCheckBox()
         // console.log(table_head)
         $("#data-entity-tbl>thead").append(table_head);
         
      },
      error: function (error) {
         bootbox.alert("Cannot connect cluster please try again");
      }
  });
}

function setDatatable(){
   // var dataArray = [
   //    {
   //      id: "8",
   //      name: "Rhona Davidson",
   //      position: "Integration Specialist",
   //      salary: "$327,900",
   //      start_date: "2010/10/14",
   //      office: "Tokyo",
   //      extn: "6200",
   //    },
   //    {
   //      id: "9",
   //      name: "Colleen Hurst",
   //      position: "Javascript Developer",
   //      salary: "$205,500",
   //      start_date: "2009/09/15",
   //      office: "San Francisco",
   //      extn: "2360",
   //    },
   //    {
   //      id: "10",
   //      name: "Sonya Frost",
   //      position: "Software Engineer",
   //      salary: "$103,600",
   //      start_date: "2008/12/13",
   //      office: "Edinburgh",
   //      extn: "1667",
   //    },
   //    {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   //     {
   //       id: "10",
   //       name: "Sonya Frost",
   //       position: "Software Engineer",
   //       salary: "$103,600",
   //       start_date: "2008/12/13",
   //       office: "Edinburgh",
   //       extn: "1667",
   //     },
   // ];
   // var table = $("#data-entity-tbl").dataTable({
   //    data: dataArray,
   //    columns: [
   //      { data: "name" },
   //      { data: "position" },
   //      { data: "office" },
   //      { data: "extn" },
   //      { data: "start_date" },
   //      { data: "salary" },
   //    ],
   // });
   var info = table.page.info();
   // console.log(table.page);
   // $('#data-entity-tbl').html(
   //    'Currently showing page '+(info.page+1)+' of '+info.pages+' pages.'
   // );
   // console.log('data after pop');
   // console.log(data_test);
   // // console.log(dataArray);
   // data_test.pop();
   // data_test.pop();
   // // console.log(data);
   // // // console.log(data.pop());
   // $('#data-entity-tbl').DataTable({
   //    processing: true,
   //    pageLength: 10,
   //    data: data_test,
   //    // responsive: true,
   //    // processing: true,
   //    // serverSide: true,
   //    // pageLength: 10,
   //    columns: [
   //       { data: "dl_data_dt"},
   //       { data: "allborrowerncbrequested" },
   //       { data: "applicationclass" },
   //       { data: "applicationdate" },
   //       { data: "applicationtype" },
   //       { data: "campaigncode" },
   //       { data: "campaigncodedescription" },
   //       { data: "customername" },
   //       { data: "isshortregister" },
   //       { data: "noofvehicle" },
   //       { data: "producttype" },
   //       { data: "producttypedesc" },
   //       { data: "referenceno" },
   //       { data: "pyslaname" },
   //       { data: "pystatuswork" },
   //    ],
   // })
}

$("#btn-search-entity").click(function(){
   bot_abbr = $("#data-entity-name option:selected").text();
   bot_abbr_mod = bot_abbr.split('(');
   bot_abbr_mod = bot_abbr_mod[1].replace(')', '');
   console.log(bot_abbr_mod);
   product = $("#product option:selected").text();
   createCriteriaSections(bot_abbr_mod);
   setFrequency();
   setDatepicker();
   $('#criteriaSelect1').on('change', function(){
      // console.log("frequency_change");
      // let optionSelected = $("#criteriaSelect1 option:selected", this).text();
      setDatepicker();
   });
   // $('#btn-criteria-div').show();
});

$("#data-entity-group").change(function(){
   setEntityName();
});

$("#btn-criteria").click(function(){
   let response = [];
   let current_bot_abbr = $("#data-entity-name option:selected").text();
   let current_bot_abbr_mod = current_bot_abbr.split('(');
   current_bot_abbr_mod = current_bot_abbr_mod[1].replace(')', '');
   // console.log(bot_abbr_mod);
   // console.log(current_bot_abbr_mod);
   if(current_bot_abbr_mod == bot_abbr_mod){
      if(validateFields()){
         var start = new Date().toLocaleTimeString();
         console.log("Start Time: " + start);
         $('#content-view-data-entity').show();
         // setDatatable();
         // setCheckBox();
         // console.log($('.paginate_button page-item active .page-link').text())
         $("#data-entity-tbl").empty();
         $("#data-entity-tbl>thead").empty();
         $("#data-entity-tbl>tbody").empty();
         // $("#data-entity-tbl").append('<thead class="thead-dark text-nowrap"></thead>');
         // $("#data-entity-tbl").append('<tbody class="text-nowrap" width="100%"></tbody>');
         getDescription();
         // var json_column = JSON.parse('{ data: "bsns_dt"},{ data: "organization_id" },{ data: "data_date" },{ data: "counterparty_id" },{ data: "identification_type" },{ data: "identification_type_country" },{ data: "identification_number" },{ data: "branch_fi_code"}')
         
         
         var table = $('#data-entity-tbl').DataTable({
            "serverSide": true,
            "processing": true,
            "language": {
               search: '<i class="fas fa-search"></i>',
               searchPlaceholder: 'Search'
            },
         //    "bInfo" : false,
         //    'columnDefs': [
         //       {
         //         'targets': 0,
         //         'checkboxes': {
         //            'selectRow': true
         //         }
         //      }
         //    ],
         //   'select': {
         //      'style': 'multi'
         //    },
         //   'order': [[1, 'asc']],
            // "paging": true,
            // "pageLength": 10,
            // data: data_test,
            // "responsive": true,
            // processing: true,
            // serverSide: true,
            // "pageLength": 10,
            "ajax": {
               type: "POST",
               url: "get_config_result",
               headers: {'X-CSRFToken': CSRF_TOKEN},
               data: {
                  'entity_fields': JSON.stringify(obj),
                  'bot_abbr': bot_abbr_mod,
                  'product': product
               },
               // success: function (data) {
               //    response = data;
               //    console.log(data);
               // }
            },
            // "columns": [
            //    { data: "dl_data_dt"},
            //    { data: "allborrowerncbrequested" },
            //    { data: "applicationclass" },
            //    { data: "applicationdate" },
            //    { data: "applicationtype" },
            //    { data: "campaigncode" },
            //    { data: "campaigncodedescription" },
            //    { data: "customername" },
            //    { data: "isshortregister" },
            //    { data: "noofvehicle" },
            //    { data: "producttype" },
            //    { data: "producttypedesc" },
            //    { data: "referenceno" },
            //    { data: "pyslaname" },
            //    { data: "pystatuswork" },
            // ],

            // "columns": titleArray,"data": array,

            "columns": [
               { data: "bsns_dt"},
               { data: "organization_id" },
               { data: "data_date" },
               { data: "counterparty_id" },
               { data: "identification_type" },
               { data: "identification_type_country" },
               { data: "identification_number" },
               { data: "branch_fi_code"},
            ],
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
            "bDestroy": true,
         });
         $("#data-entity-tbl>thead").addClass("thead-dark text-nowrap");
         $("#data-entity-tbl>tbody").addClass("text-nowrap width='100%'");
         $("#data-entity-tbl>thead>tr").hide();
         // getDescription();
         // let test = [{'count': 1, 'bsns_dt': datetime.date(2021, 6, 30), 'organization_id': '014', 'data_date': datetime.date(2021, 6, 30), 'counterparty_id': '001400000000000000000000000036', 'identification_type': '2002700001', 'identification_type_country': 'TH', 'identification_number': '4919759453119', 'branch_fi_code': None}]

         
      //    $.ajax({
      //       type: "POST",
      //       url: "get_config_result",
      //       data: {
      //           'entity_fields': JSON.stringify(obj),
      //           'bot_abbr': bot_abbr_mod,
      //           'product': product
      //       },
      //       datatype: 'json',
      //       beforeSend: function (xhr) {
      //           xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
      //           // show image container
      //          //  $('#content-view-data-entity').show();
      //           $("#loading").attr("style", "visibility: visible;");
      //       },
      //       complete: function (data) {
      //           // Hide image container
      //           $("#loading").attr("style", "visibility: hidden;");
      //       },
      //       success: function (data) {
      //          console.log(data);
      //          // console.log(criteria_json);
      //          // console.log(data[data.length-1]['job_sts']);
      //          // setValidationStatus(data);
      //          $("#data-entity-tbl").empty();
      //          $("#data-entity-tbl>thead").empty();
      //          $("#data-entity-tbl>tbody").empty();
      //          // setDatatable(data);
      //          // $("#data-entity-tbl").append('<thead class="thead-dark text-nowrap"></thead>');
      //          // $("#data-entity-tbl").append('<tbody class="text-nowrap" width="100%"></tbody>');
      //          // let table_head = '';
      //          // let table_head_info = '';
      //          // let table_row = '';
      //          // let table_row_info = '';
      //          // table_head += '<tr><th></th>';
      //          // table_head_info += '<th>' + 'dl_data_dt' + '</th>';
      //          // // console.log(data[data.length-2]['elm_desc']);
               
      //          // // display keys
      //          // // console.log(data[0]);
      //          // // for(let x in data[0]){
      //          // //    console.log(x);
      //          // // }
               
      //          // for(let i=0;i<data[data.length-2]['elm_desc'].length;i++){
      //          //    table_head_info += '<th>' + data[data.length-2]['elm_desc'][i] + '</th>';
      //          //    // console.log(data[data.length-2]['elm_desc'][i]);
      //          //    // console.log(Object.keys(data[0])[i]);
      //          // }
   
      //          // table_head += table_head_info + '</tr>';
      //          // // console.log(table_head)
      //          // $("#data-entity-tbl>thead").append(table_head);
      //          // table_head = '';
      //          // table_head_info = '';
      //          // console.log(data.length);
      //          // // setDatatable(data);
      //          // $("#data-entity-tbl>tbody").append('<td></td>');
      //          // for(let i=0;i<data.length-2;i++){
      //          //    table_row += '<tr><td></td>'
      //          //    for(let j=0;j<Object.keys(data[i]).length;j++){
      //          //       table_row_info += '<td>' + Object.values(data[i])[j] + '</td>';
      //          //    }
      //          //    // $("#example>tbody").append('</tr>')
      //          //    table_row += table_row_info + '</tr>';
      //          //    // console.log(table_row);
      //          //    $("#data-entity-tbl>tbody").append(table_row);
      //          //    table_row = '';
      //          //    table_row_info = '';
      //          // }
      //          // setCheckBox();
      //          // calculateTotalRecords(data);
      //          // $('#content-view-data-entity').show();
      //          // var end = new Date().toLocaleTimeString();
      //          // // var time = end - start;
      //          // console.log("End Time: " + end);
      //          // // console.log("Total Time: " + time);
      //       },
      //       error: function (error) {
      //          bootbox.alert("Cannot connect cluster please try again");
      //       }
      //   });
      }
   }
   else{
      bootbox.alert({
         message: 'Current Data Entity Name (' + current_bot_abbr_mod + ') ' + 'does not match with Entity name (' + bot_abbr_mod + ')',
         centerVertical: true
      });
   }
});
// function getProduct(){
//    $.ajax({
//       type: "POST",
//       url: "get_product",
//       datatype: 'json',
//       beforeSend: function (xhr) {
//           xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
//           // show image container
//          //  $("#loadingView").attr("style", "visibility: visible;");
//       },
//       complete: function (data) {
//           // Hide image container
//          //  $("#loadingView").attr("style", "visibility: hidden;");
//       },
//       success: function (data) {
//          console.log(data)
//          for(let i=0;i<data[0]['ProductCode'].length;i++){
//             $("#exampleSelect3").append('<option value="' + data[0]['ProductCode'][i] + '">' + data[0]['ProductName'][i] + '</option>')
//          }
//           //when ajax is running correctly
          
//       },
//       error: function (error) {
//           alert("Somthing went wrong!!");
//       }
//    });
// }

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
// var table = $('#example').DataTable({
//     "language": {
//         search: '<i class="fas fa-search"></i>',
//         searchPlaceholder: 'Search'
//     },
//     "bInfo" : false,
//     'columnDefs': [
//        {
//           'targets': 0,
//           'checkboxes': {
//              'selectRow': true
//           }
//        }
//     ],
//     'select': {
//        'style': 'multi'
//     },
//     'order': [[1, 'asc']]
//  });
// $("#data-entity-tbl_wrapper").addClass("ml-4");

$("#data-entity-tbl").parent().css({"overflow":"auto"})

$('#datepicker').datepicker({
   uiLibrary: 'bootstrap4'
});