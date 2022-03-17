///// Global variable Section /////
var timeoutInMiliseconds = 900000; // 15 minutes log out => 60000 for test
var timeoutId;
var permission_menu = ['customer_menu','targetfunnel_menu','task_menu','schedule_menu','campaignplanning_menu','campaignplanning_todolist_sub_menu','campaignplanning_summary_sub_menu','campaignplanning_report_sub_menu','campaignplanning_master_sub_menu','portal_menu','portal_portfolio_sub_menu','portal_master_sub_menu']
var targetfunnel_element = {
  'targetfunnel_manage':'new_inquiry_btn,save_inquiry_condition_btn,edit_inquiry_info',
  'targetfunnel_execute':'execute',
  'targetfunnel_tab_inclusion':'pills-step1-tab',
  'targetfunnel_tab_exclusion':'pills-step2-tab',
  'targetfunnel_tab_basic_exclusion':'pills-step3-tab',
  'targetfunnel_tab_export':'pills-step4-tab',
  'targetfunnel_modal_basic_ex_detail':'basic_ex_detail',
  'targetfunnel_modal_segment_income_digital_channel':'segment_income_digital_channel',
  'targetfunnel_section_inclusion_upload_list':'section1',
  'targetfunnel_section_inclusion_criteria':'section2',
  'targetfunnel_section_exclusion_upload_list':'section3',
  'targetfunnel_section_exclusion_criteria':'section4',
  'targetfunnel_button_export':'label_export_with_header,export',
  'targetfunnel_button_preview':'preview',
}
var tap_element = {
  1 : 'pills-step1',
  2 : 'pills-step2',
  3 : 'pills-step3',
  4 : 'pills-step4'
}
var campaignplaning_element ={
  'campaignplanning_summary_button_export':'search_export',
  'campaignplanning_summary_button_new':'create_campaign_button',
  'campaignplanning_summary_button_booking':'booking_campaign_button',
  'campaignplanning_summary_button_save':'savedraft_campaign,submit_campaign',
  'campaignplanning_report_segment_product':'segment_product_report_card',
  'campaignplanning_report_planning_executor':'campaign_plan_and_manage_card',
  'campaignplanning_report_commu_by_executor':'communication_plan_card',
}

var portal_element = {
  'portal_portfolio_button_new': 'create_project_button',
  'portal_portfolio_button_save': 'submit_project',
  'portal_portfolio_button_export': 'search_export',
  'portal_portfolio_button_generate_ideasolution_email': 'generate_email_btt',
}
///// End Global variable Section /////

///// Event Function Section /////
$(document).ready(function() {
  setupTimers();
  $("#sidebarCollapse").on("click", function() {
    $("#sidebar").toggleClass("active");
  });
  set_permission();
});
///// End Event Function Section /////

 ///// Event Function Section /////
function startTimer() { 
    timeoutId1 = window.setTimeout(setsession, 870000); // before 15 minutes => 55000 for test
    timeoutId = window.setTimeout(doInactive, timeoutInMiliseconds);
}

function resetTimer() { 
  window.clearTimeout(timeoutId);
  window.clearTimeout(timeoutId1);
  startTimer();

  window.localStorage.setItem("Status", "Active");
  const last_active = new Date();
  window.localStorage.setItem("Last_active", last_active);
}

function setsession() {
  window.localStorage.setItem("Status", "Timeout");
}

function doInactive() {
  
      last_active = window.localStorage.getItem("Last_active");

      last_active_time = new Date(last_active);
      now_time = new Date();
      
      msecdiff = now_time.getTime() - last_active_time.getTime();
      
      if(window.localStorage.getItem("Status") == "Timeout" && msecdiff >= 900000){ // 60000 for test in 1 minute
        var url_origin = $(location).attr('origin');
        $.ajax({
          url: url_origin + '/logout/',
          method: "GET",
          data : "logout",
          success: function () {
            window.location.href = url_origin + '/login/';
            return true
          },
          error: function() {
            return false
          }
        });
      }
      else{
        newmillisectime = 900000 - msecdiff ; // 60000 for test in 1 minute
        window.setTimeout(doInactive, newmillisectime);
      }   
}
 
function setupTimers () {
    document.addEventListener("mousemove", resetTimer, false);
    document.addEventListener("mousedown", resetTimer, false);
    document.addEventListener("keypress", resetTimer, false);
    document.addEventListener("touchmove", resetTimer, false);
    document.addEventListener("scroll", resetTimer, false);
     
    startTimer();
}

function set_permission(){

  $.ajax({
    type: "POST",
    url: "userPermission",
    data: {
      input_key: "rm_id"
    },
    datatype: "json",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
    },
    success: function (data) {
      manage_permission(data);
    },
    error: function (error) {
      alert("error:" + eval(error));
    }
  }); //end ajax 2
}

function manage_permission(permission){
  var permissionarr = permission;
  var path = $(location).attr('pathname');
  var dss_port = path.includes("/dss-portal/project");
  
  // Set Menu permission
  for(const menu in permission_menu){
    if (permissionarr.includes(permission_menu[menu])){
      $('#'+permission_menu[menu]).removeAttr('hidden');
    }else{
      $('#'+permission_menu[menu]).remove();
    }
  }
 
  // Set Permission of Target Funnel Page
  if(path == '/targetfunnel/'){
    tap_arr = check_and_remove_permission(permissionarr, targetfunnel_element);
    manageTap(tap_arr);
  }

  // Set Permission of Campaign Planning Page
  if(path == '/campaignplanning/todo'){
    check_and_remove_permission(permissionarr, campaignplaning_element);
  }
  if(path == '/campaignplanning/campaign_summary'){
    check_and_remove_permission(permissionarr, campaignplaning_element);
    $("#search_form").attr("style", "visibility: visible;");
    $("#loading_search_summary").attr("style", "visibility: hidden;");
  }
  if(path == '/campaignplanning/campaignReport'){
    check_and_remove_permission(permissionarr, campaignplaning_element);
    $("#loading").attr("style", "visibility: hidden;");
    $("#report_card_list").attr("style", "visibility: visible;");
  }
  if(dss_port == true){
    check_and_remove_permission(permissionarr, portal_element);
    $("#search_form").attr("style", "visibility: visible;");
  }
}

function check_and_remove_permission(permissionarr, permission_element){
  var taparr = [];

  for (const permission_id in permission_element) {
    id = permission_element[permission_id];

    if(!permissionarr.includes(permission_id)) {
      
      if(id.includes(",")){
        id_elem = id.split(',');
        id_elem.forEach(removeElement);
        
      }else{
        $('#'+id).remove();
      }
    }else{

      if(id.includes("tab")){
        var thenum = id.replace( /[^0-9]/g, '');
        taparr.push(parseInt(thenum));
      }
    }
  }
  
  return taparr;
}

function removeElement(item, index){
  $('#'+item).remove();
}

function manageTap(arr){
  for (const tap in tap_element) {

    if(!arr.includes(parseInt(tap))){ 
      $('#'+tap_element[parseInt(tap)]).attr('hidden','hidden');
    }
  }

  if(arr.length >= 1){
    arr.sort();  
    
    $('#'+'pills-step'+arr[0]+'-tab').addClass("active");
    $('#'+tap_element[arr[0]]).addClass("show active");  
    $('#'+'pills-step'+arr[0]+'-tab').attr("aria-selected","true");  
  }
}

function numberWithCommas(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function numberRemoveCommas(num) {
  return num.replace(/,/g, '');
};

///// End Custom Function Section /////