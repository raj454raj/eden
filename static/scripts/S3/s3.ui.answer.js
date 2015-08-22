(function($, undefined) {
    "use strict";
    var addAnswerID = 0;

    $.widget('s3.addAnswer', {

        options: {

        },

        /**
         * Create the widget
         */
        _create: function(){
            this.id = addAnswerID;
            addAnswerID += 1;
            this.namespace = '.addAnswer';
        },

        /**
         * Initialize the widget
         */
        _init: function() {
            console.log(this);
        },
    });

})(jQuery);
