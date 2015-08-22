# -*- coding: utf-8 -*-

""" Sahana Eden Data Collection Models

    @copyright: 2014-2015 (c) Sahana Software Foundation
    @license: MIT

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    @status: experimental, WIP
"""

__all__ = ("DataCollectionTemplateModel",
           "DataCollectionModel",
           "dc_rheader",
           )

from gluon import *

from ..s3 import *
from s3layouts import S3PopupLink

# =============================================================================
class DataCollectionTemplateModel(S3Model):

    names = ("dc_template",
             "dc_template_id",
             "dc_question",
             "dc_question_id",
             "dc_template_question",
             "dc_question_l10n",
             )

    def model(self):

        T = current.T
        db = current.db

        crud_strings = current.response.s3.crud_strings

        define_table = self.define_table
        add_components = self.add_components

        # =====================================================================
        # Data Collection Template
        #
        tablename = "dc_template"
        define_table(tablename,
                     Field("name",
                           requires = IS_NOT_EMPTY(),
                           ),
                     # Whether to show this template in the form list
                     # (required since form list can't use authorization)
                     Field("public", "boolean",
                           default = False,
                           ),
                     s3_comments(),
                     *s3_meta_fields())

        self.configure(tablename,
                       xform = {"collection": "dc_collection",
                                "questions": "question",
                                "answers": "answer",
                                },
                       )
        # Represent
        represent = S3Represent(lookup=tablename)

        # Reusable field
        template_id = S3ReusableField("template_id", "reference %s" % tablename,
                                      label = T("Template"),
                                      represent = represent,
                                      requires = IS_ONE_OF(db, "dc_template.id",
                                                           represent,
                                                           ),
                                      sortby = "name",
                                      comment = S3PopupLink(f="template",
                                                            tooltip=T("Add a new data collection template"),
                                                            ),
                                      )

        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Create Template"),
            title_display = T("Template Details"),
            title_list = T("Templates"),
            title_update = T("Edit Template"),
            title_upload = T("Import Templates"),
            label_list_button = T("List Templates"),
            label_delete_button = T("Delete Template"),
            msg_record_created = T("Template added"),
            msg_record_modified = T("Template updated"),
            msg_record_deleted = T("Template deleted"),
            msg_list_empty = T("No Templates currently registered"))

        # Components
        add_components(tablename,
                       dc_question = {"link": "dc_template_question",
                                      "joinby": "template_id",
                                      "key": "question_id",
                                      "actuate": "hide",
                                      "autodelete": False,
                                      },
                       )

        # =====================================================================
        # Data Collection Question
        #
        tablename = "dc_question"
        define_table(tablename,
                     Field("question",
                           requires = IS_NOT_EMPTY(),
                           ),
                     Field("model", "json",
                           requires = IS_EMPTY_OR(IS_JSON(native_json=True)),
                           # @todo: representation?
                           widget = S3QuestionWidget(),
                           ),
                     *s3_meta_fields())

        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Create Question"),
            title_display = T("Question Details"),
            title_list = T("Questions"),
            title_update = T("Edit Question"),
            title_upload = T("Import Questions"),
            label_list_button = T("List Questions"),
            label_delete_button = T("Delete Question"),
            msg_record_created = T("Question added"),
            msg_record_modified = T("Question updated"),
            msg_record_deleted = T("Question deleted"),
            msg_list_empty = T("No Questions currently registered"))

        # Represent
        represent = S3Represent(lookup=tablename,
                                fields=["question"],
                                show_link=True,
                                )

        # Reusable field
        question_id = S3ReusableField("question_id", "reference %s" % tablename,
                                      label = T("Question"),
                                      represent = represent,
                                      requires = IS_ONE_OF(db, "dc_question.id",
                                                           represent,
                                                           ),
                                      sortby = "name",
                                      comment = S3PopupLink(f="question",
                                                            tooltip=T("Add a new data collection question"),
                                                            ),
                                      )

        # Components
        add_components(tablename,
                       dc_question_l10n = "question_id",
                       )

        # =====================================================================
        # Template <=> Question link table
        #
        tablename = "dc_template_question"
        define_table(tablename,
                     template_id(),
                     question_id(),
                     *s3_meta_fields())

        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Add Question"),
            label_delete_button = T("Remove Question"),
            msg_record_created = T("Question added"),
            msg_record_deleted = T("Question remove"),
            msg_list_empty = T("No Questions currently registered"))

        # =====================================================================
        # Questions l10n
        #
        tablename = "dc_question_l10n"
        define_table(tablename,
                     question_id(ondelete = "CASCADE",
                                 ),
                     Field("language",
                           label = T("Language"),
                           represent = IS_ISO639_2_LANGUAGE_CODE.represent,
                           requires = IS_ISO639_2_LANGUAGE_CODE(sort=True),
                           ),
                     Field("question",
                           requires = IS_NOT_EMPTY(),
                           ),
                     Field("model", "json",
                           requires = IS_EMPTY_OR(IS_JSON()),
                           # @todo: representation?
                           # @todo: widget?
                           ),
                     s3_comments(),
                     *s3_meta_fields())

        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Create Translation"),
            title_display = T("Translation"),
            title_list = T("Translations"),
            title_update = T("Edit Translation"),
            title_upload = T("Import Translations"),
            label_list_button = T("List Translations"),
            label_delete_button = T("Delete Translation"),
            msg_record_created = T("Translation added"),
            msg_record_modified = T("Translation updated"),
            msg_record_deleted = T("Translation deleted"),
            msg_list_empty = T("No Translations currently available"))

        # =====================================================================
        # Pass names back to global scope (s3.*)
        return dict(dc_template_id = template_id,
                    dc_question_id = question_id,
                    )

    # -------------------------------------------------------------------------
    @staticmethod
    def defaults():
        """ Safe defaults for names in case the module is disabled """

        dummy = S3ReusableField("dummy_id", "integer",
                                readable = False,
                                writable = False,
                                )

        return dict(dc_template_id = lambda **attr: dummy("template_id"),
                    dc_question_id = lambda **attr: dummy("question_id"),
                    )

# =============================================================================
class DataCollectionModel(S3Model):

    names = ("dc_collection",
             "dc_question_collection",
             )

    def model(self):

        T = current.T
        db = current.db

        crud_strings = current.response.s3.crud_strings

        define_table = self.define_table

        # =====================================================================
        # Data Collection
        #
        tablename = "dc_collection"
        define_table(tablename,
                     self.super_link("doc_id", "doc_entity"),
                     self.dc_template_id(),
                     s3_date(default = "now"),
                     self.gis_location_id(),
                     self.org_organisation_id(),
                     self.pr_person_id(
                        default = current.auth.s3_logged_in_person(),
                     ),
                     s3_comments(),
                     *s3_meta_fields())

        # Configuration
        self.configure(tablename,
                       onaccept = self.dc_collection_onaccept,
                       orderby = "dc_collection.date desc",
                       super_entity = "doc_entity",
                       )

        # Custom method for dc_collection
        self.set_method("dc", "collection",
                        method="answers",
                        action=dc_AnswerMethod())

        # Components
        self.add_components(tablename,
                            dc_question = {"link": "dc_question_collection",
                                           "joinby": "collection_id",
                                           "key": "question_id",
                                           "actuate": "hide"},
                            )

        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Create Data Collection"),
            title_display = T("Data Collection Details"),
            title_list = T("Data Collections"),
            title_update = T("Edit Data Collection"),
            title_upload = T("Import Data Collections"),
            label_list_button = T("List Data Collections"),
            label_delete_button = T("Delete Data Collection"),
            msg_record_created = T("Data Collection added"),
            msg_record_modified = T("Data Collection updated"),
            msg_record_deleted = T("Data Collection deleted"),
            msg_list_empty = T("No Data Collections currently registered"))

        # @todo: representation including template name, location and date
        #        (not currently required since always hidden)
        represent = S3Represent(lookup=tablename,
                                fields=["date"],
                                )

        # Reusable field
        collection_id = S3ReusableField("collection_id", "reference %s" % tablename,
                                        label = T("Data Collection"),
                                        represent = represent,
                                        requires = IS_ONE_OF(db, "dc_collection.id",
                                                             represent,
                                                             ),
                                        comment = S3PopupLink(f="collection",
                                                              tooltip=T("Add a new data collection"),
                                                              ),
                                        )

        # =====================================================================
        # Data Collection Question
        #
        # The table acts like a link table between dc_collection and dc_question
        tablename = "dc_question_collection"
        define_table(tablename,
                     collection_id(),
                     self.dc_question_id(),
                     Field("answer", "json",
                           requires=IS_EMPTY_OR(IS_JSON()),
                           default={},
                           readable=False,
                           writable=False,
                           # @todo: representation? (based the question model)
                           # @todo: widget? (based the question model)
                           ),
                     *s3_meta_fields())

        # These CRUD strings correspond to adding question to the collection
        # These are shown while a collection is opened
        # Direct CRUD on dc_question_collection is not allowed
        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Add Question to Collection"),
            title_display = T("Question Details"),
            title_list = T("Questions"),
            title_update = T("Edit Question"),
            title_upload = T("Import Questions"),
            label_list_button = T("List Questions"),
            label_delete_button = T("Delete Question"),
            msg_record_created = T("Question added to Collection"),
            msg_record_modified = T("Question updated"),
            msg_record_deleted = T("Question deleted from Collection"),
            msg_list_empty = T("No Questions currently registered"))

        # =====================================================================
        # Pass names back to global scope (s3.*)
        return dict(dc_collection_id = collection_id,
                    )

    # -------------------------------------------------------------------------
    def dc_collection_onaccept(self, form):
        """
            Create dc_question_collection records with empty
            answer fields.
            Updating these records with actual answers is done
            by answers method
        """

        db = current.db
        qctable = db.dc_question_collection
        ttable = db.dc_template
        tqtable = db.dc_template_question

        # Collection ID
        record_id = form.vars.id

        # Template ID
        template_id = form.vars.template_id

        # Left join query to combine dc_template and dc_template_question
        left = [ttable.on(tqtable.template_id == ttable.id)]

        questions = db(ttable.id == template_id).select(tqtable.question_id,
                                                        left=left)

        # Iterate through the questions of the selected template
        # and add an empty dc_question_collection record
        for question in questions:
            answer_id = qctable.insert(collection_id=record_id,
                                       question_id=question.question_id,
                                       )
        return

    # -------------------------------------------------------------------------
    @staticmethod
    def defaults():
        """ Safe defaults for names in case the module is disabled """

        dummy = S3ReusableField("dummy_id", "integer",
                                readable = False,
                                writable = False,
                                )

        return dict(dc_collection_id = lambda **attr: dummy("collection_id"),
                    )

# =============================================================================
def dc_rheader(r, tabs=None):
    """ Resource Headers for Data Collection Tool """

    T = current.T
    if r.representation != "html":
        return None

    resourcename = r.name

    if resourcename == "template":

        tabs = ((T("Basic Details"), None),
                (T("Questions"), "question"),
                )

        rheader_fields = (["name"],
                          )
        rheader = S3ResourceHeader(rheader_fields, tabs)(r)

    elif resourcename == "question":

        tabs = ((T("Question Details"), None),
                (T("Translations"), "question_l10n"),
                )

        rheader_fields = (["question"],
                          )
        rheader = S3ResourceHeader(rheader_fields, tabs)(r)

    elif resourcename == "collection":

        tabs = ((T("Basic Details"), None),
                (T("Questions"), "question"),
                (T("Answers"), "answers"),
                (T("Attachments"), "document"),
                )

        rheader_fields = (["template_id"],
                          ["location_id"],
                          ["date"],
                          )
        rheader = S3ResourceHeader(rheader_fields, tabs)(r)

    else:
        rheader = ""

    return rheader

# =============================================================================
class dc_AnswerMethod(S3Method):
    """
        Answer method which renders widget for
        questions created in template or explicitly
    """

    # -------------------------------------------------------------------------
    def apply_method(self, r, **attr):
        """
            Apply method.

            @param r: the S3Request
            @param attr: controller options for this request
        """

        s3 = current.response.s3
        db = current.db
        qctable = db.dc_question_collection
        # The record id will be collection_id since
        # Answer method is applied on the master resource
        collection_id = r.id

        # Retrieve all the questions associated with the collection
        # Note => These will contain questions from -
        #      1. The template selected for the collection
        #      2. Any other records added explicitly by the
        #         user from the Questions component
        query = (qctable.collection_id == collection_id)
        questions = db(query).select(qctable.question_id)
        question_ids = map(lambda x: int(x["question_id"]), questions)

        # Output to views
        output = {}

        # Widget ID
        widget_id = "dc_answer_model"
        output["widget_id"] = widget_id

        # div that will contain the answer widget
        placeholder_div = DIV(_id=widget_id)
        output["placeholder_div"] = placeholder_div

        self.inject_script(widget_id)

        # Hidden input containing collection_id
        input_collection_id = INPUT(_type="hidden",
                                    _id="collection-id",
                                    _value=collection_id)

        # Hidden input containing question_ids
        input_question_ids = INPUT(_type="hidden",
                                   _id="question-ids",
                                   _value=question_ids)

        # Embed hidden inputs in an empty tag
        hidden_content = TAG[""](input_collection_id, input_question_ids)
        output["hidden_content"] = hidden_content

        # Title string should be for updating a particular collection
        output["title"] = self.crud_string(r.tablename, "title_update")

        return output

    # -------------------------------------------------------------------------
    @staticmethod
    def inject_script(widget_id, options=None):
        """
            Inject the groupedItems script and bind it to the container
            @param widget_id: the widget container DOM ID
            @param options: dict with options for the widget
            @note: options dict must be JSON-serializable
        """

        s3 = current.response.s3

        scripts = s3.scripts
        appname = current.request.application

        # Inject UI widget script
        # @ToDo: Add s3.debug condition after generating s3.ui.answer.min.js
        script = "/%s/static/scripts/S3/s3.ui.answer.js" % appname
        if script not in scripts:
            scripts.append(script)

        # Inject widget instantiation
        if not options:
            options = {}

        script = """$("#%(widget_id)s").addAnswer(%(options)s)""" % \
                    {"widget_id": widget_id,
                     "options": json.dumps(options),
                     }

        s3.jquery_ready.append(script)

# END =========================================================================
