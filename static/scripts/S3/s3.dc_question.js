/*
 * Used by the Question Form(controllers/dc.py)
 * This script is in Static to allow caching
 * Dynamic constants (e.g. Internationalised strings) are set in server-generated script
 */

// Module pattern to hide internal vars
(function () {

    // A JSON to convert question type
    // from integer to actual string 
    var type_json = {1: "String",
                     2: "Integer",
                     3: "Float",
                     4: "Object",
                     5: "Date",
                     6: "Time",
                     7: "DateTime",
                     8: "Reference",
                     9: "Location"
                     };

    // Function to hide input fields based
    // on the selection of question type
    var update_form = function() {
        var type = $("#dc_question_type").val();
        type = type_json[type];

        if (type === "Integer" || type === "Float") {

            $("#dc_question_max__row").show();
            $("#dc_question_min__row").show();
            $("#dc_question_reference__row").hide();
            $("#dc_question_represent__row").hide();
            $("#dc_question_filter__row").hide();
            $("#dc_question_location_fields__row").hide();
            $("#dc_question_options__row").hide();
            $("#dc_question_multiple__row").hide();

        } else if (type === "String") {
            
            $("#dc_question_max__row").hide();
            $("#dc_question_min__row").hide();
            $("#dc_question_reference__row").hide();
            $("#dc_question_represent__row").hide();
            $("#dc_question_filter__row").hide();
            $("#dc_question_location_fields__row").hide();
            $("#dc_question_options__row").hide();
            $("#dc_question_multiple__row").hide();

        } else if (type === "Object") {
            
            $("#dc_question_max__row").hide();
            $("#dc_question_min__row").hide();
            $("#dc_question_reference__row").hide();
            $("#dc_question_represent__row").hide();
            $("#dc_question_filter__row").hide();
            $("#dc_question_location_fields__row").hide();
            $("#dc_question_options__row").show();
            $("#dc_question_multiple__row").show();

        } else if (type === "Date" || type === "Time" || type === "DateTime") {
            
            $("#dc_question_max__row").show();
            $("#dc_question_min__row").show();
            $("#dc_question_reference__row").hide();
            $("#dc_question_represent__row").hide();
            $("#dc_question_filter__row").hide();
            $("#dc_question_location_fields__row").hide();
            $("#dc_question_options__row").hide();
            $("#dc_question_multiple__row").hide();
            
        } else if (type === "Reference") {
            
            $("#dc_question_max__row").hide();
            $("#dc_question_min__row").hide();
            $("#dc_question_reference__row").show();
            $("#dc_question_represent__row").show();
            $("#dc_question_filter__row").show();
            $("#dc_question_location_fields__row").hide();
            $("#dc_question_options__row").hide();
            $("#dc_question_multiple__row").hide();

        } else if (type === "Location") {
        
            $("#dc_question_max__row").hide();
            $("#dc_question_min__row").hide();
            $("#dc_question_reference__row").hide();
            $("#dc_question_represent__row").hide();
            $("#dc_question_filter__row").hide();
            $("#dc_question_location_fields__row").show();
            $("#dc_question_options__row").hide();
            $("#dc_question_multiple__row").hide();
            $("#dc_question_default_answer__row").hide();

        }

    }
    $(document).ready(function() {
        update_form();
        $("#dc_question_type").change(function() {
            update_form();
        });
    });
}());
