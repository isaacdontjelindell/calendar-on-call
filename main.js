(function ($) {
    $.fn.showHide = function (options) {
 
    //default vars for the plugin
        var defaults = {
            speed: 1000,
            easing: '',
            changeText: 0,
            showText: 'Show',
            hideText: 'Hide'
 
        };
        var options = $.extend(defaults, options);
 
        $(this).click(function () {
// optionally add the class .toggleDiv to each div you want to automatically close
                      $('.toggleDiv:hidden').slideUp(options.speed, options.easing);
             // this var stores which button you've clicked
             var toggleClick = $(this);
             // this reads the rel attribute of the button to determine which div id to toggle
             var toggleDiv = $(this).attr('rel');
             // here we toggle show/hide the correct div at the right speed and using which easing effect
             $(toggleDiv).slideToggle(options.speed, options.easing, function() {
             // this only fires once the animation is completed
             if(options.changeText==1){
             $(toggleDiv).is(":visible") ? toggleClick.text(options.hideText) : toggleClick.text(options.showText);
             }
              });
 
          return false;
 
        });
 
    };
})(jQuery);

$(document).ready(function(){
 
   $('.show_hide').showHide({
        speed: 500,  // speed you want the toggle to happen
        easing: '',  // the animation effect you want. Remove this line if you dont want an effect and if you haven't included jQuery UI
        changeText: 0, // if you dont want the button text to change, set this to 0
        showText: 'View',// the button text to show when a div is closed
        hideText: 'Close' // the button text to show when a div is open
 
    });
 
});


function validateNewContact()
{
    var name=document.forms["contactListAddForm"]["contact"].value;
    var number=document.forms["contactListAddForm"]["phone"].value;
    console.log(number);
    console.log(name);
    if (name==null || name=="")
    {
        alert("A Name Must be Given");
        return false;
    }
    var format = "999-999-9999";
    var r = RegExp("^(" +
        format
            .replace(/([\(\)])/g, "\\$1")
            .replace(/9/g,"\\d") +
        ")$");
    if(! r.test(number))
    {
        alert("The Number Entered is not in the correct format");
        return false;
    }

    return true
}

function validateNewLocation()
{
    var locName=document.forms["newLocation"]["name"].value;
    var calender=document.forms["newLocation"]["cal"].value;
    var twilio_id=document.forms["newLocation"]["twilio_id"].value;
    var contacts=document.forms["newLocation"]["contacts"].value;
    if (locName == null || locName == "") {
        alert("Location Name must be provided")
        return false
    }
    if (calender == null || calender == "") {
        alert("Calender url must be provided")
        return false
    }
    if (twilio_id == null || twilio_id == "") {
        alert("Twilio Id must be provided")
        return false
    }
    contacts = contacts.split("\n");
    for (var i = 0; i<contacts.length; i++) {
        temp = contacts[i].split(":");
        name = temp[0].replace(/^\s+|\s+$/g,'');
        number = temp [1].replace(/^\s+|\s+$/g,'');
        console.log(contacts);
        console.log("|" + name + "|")
        console.log("|" + number + "|")

        if(name == null || name == "")
        {
            alert("Each Contact Must have a name!");
            return false;
        }
        
        var format = "999-999-9999";
        var r = RegExp("^(" +
            format
                .replace(/([\(\)])/g, "\\$1")
                .replace(/9/g,"\\d") +
            ")$");
        if(! r.test(number))
        {
            alert("The Number " + number + " is not in the correct format");
            return false;
        }
    }
    return true;
}


function removeLoc(loc) 
{
    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "location");
    input.setAttribute("value", loc);

    //append to form element that you want .
    document.getElementById("removeLocationForm").appendChild(input);
    document.getElementById("removeLocationForm").submit();
}
