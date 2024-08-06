$(function () {
    /* Functions */

    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                if (btn.attr("data-target") === "#modalIncomeCreate") {
                    $("#modalIncomeCreate .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalIncomeEdit") {
                    $("#modalIncomeEdit .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalIncomeDelete") {
                    $("#modalIncomeDelete .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalExpenseCreate") {
                    $("#modalExpenseCreate .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalExpenseEdit") {
                    $("#modalExpenseEdit .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalExpenseDelete") {
                    $("#modalExpenseDelete .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalAssetCreate") {
                    $("#modalAssetCreate .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalAssetEdit") {
                    $("#modalAssetEdit .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalAssetDelete") {
                    $("#modalAssetDelete .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalLiabilityCreate") {
                    $("#modalLiabilityCreate .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalLiabilityEdit") {
                    $("#modalLiabilityEdit .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalLiabilityDelete") {
                    $("#modalLiabilityDelete .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalCategoryCreate") {
                    $("#modalCategoryCreate .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalCategoryEdit") {
                    $("#modalCategoryEdit .modal-content").html("");
                } else if (btn.attr("data-target") === "#modalCategoryDelete") {
                    $("#modalCategoryDelete .modal-content").html("");
                }
            },
            success: function (data) {
                if (btn.attr("data-target") === "#modalIncomeCreate") {
                    $("#modalIncomeCreate .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalIncomeEdit") {
                    $("#modalIncomeEdit .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalIncomeDelete") {
                    $("#modalIncomeDelete .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalExpenseCreate") {
                    $("#modalExpenseCreate .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalExpenseEdit") {
                    $("#modalExpenseEdit .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalExpenseDelete") {
                    $("#modalExpenseDelete .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalAssetCreate") {
                    $("#modalAssetCreate .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalAssetEdit") {
                    $("#modalAssetEdit .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalAssetDelete") {
                    $("#modalAssetDelete .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalLiabilityCreate") {
                    $("#modalLiabilityCreate .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalLiabilityEdit") {
                    $("#modalLiabilityEdit .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalLiabilityDelete") {
                    $("#modalLiabilityDelete .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalCategoryCreate") {
                    $("#modalCategoryCreate .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalCategoryEdit") {
                    $("#modalCategoryEdit .modal-content").html(data.html_form);
                } else if (btn.attr("data-target") === "#modalCategoryDelete") {
                    $("#modalCategoryDelete .modal-content").html(data.html_form);
                }
            }
        });
    };

    let saveForm = function () {
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    location.reload(); // reload page if form is valid
                } else {
                    if (form.attr("id") === "modalIncomeCreateForm") {
                        $("#modalIncomeCreate .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalIncomeEditForm") {
                        $("#modalIncomeEdit .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalIncomeDeleteForm") {
                        $("#modalIncomeDelete .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalExpenseCreateForm") {
                        $("#modalExpenseCreate .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalExpenseEditForm") {
                        $("#modalExpenseEdit .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalExpenseDeleteForm") {
                        $("#modalExpenseDelete .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalAssetCreateForm") {
                        $("#modalAssetCreate .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalAssetEditForm") {
                        $("#modalAssetEdit .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalAssetDeleteForm") {
                        $("#modalAssetDelete .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalLiabilityCreateForm") {
                        $("#modalLiabilityCreate .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalLiabilityEditForm") {
                        $("#modalLiabilityEdit .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalLiabilityDeleteForm") {
                        $("#modalLiabilityDelete .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalCategoryCreateForm") {
                        $("#modalCategoryCreate .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalCategoryEditForm") {
                        $("#modalCategoryEdit .modal-content").html(data.html_form);
                    } else if (form.attr("id") === "modalCategoryDeleteForm") {
                        $("#modalCategoryDelete .modal-content").html(data.html_form);
                    }
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create Income
    $(".js-create-income").click(loadForm);
    $("#modalIncomeCreate").on("submit", ".js-income-create-form", saveForm);

    // Edit Income
    $(".js-edit-income").click(loadForm);
    $("#modalIncomeEdit").on("submit", ".js-income-edit-form", saveForm);

    // Delete Income
    $(".js-delete-income").click(loadForm);
    $("#modalIncomeDelete").on("submit", ".js-income-delete-form", saveForm);

    // Create Expense
    $(".js-create-expense").click(loadForm);
    $("#modalExpenseCreate").on("submit", ".js-expense-create-form", saveForm);

    // Edit Expense
    $(".js-edit-expense").click(loadForm);
    $("#modalExpenseEdit").on("submit", ".js-expense-edit-form", saveForm);

    // Delete Expense
    $(".js-delete-expense").click(loadForm);
    $("#modalExpenseDelete").on("submit", ".js-expense-delete-form", saveForm);

    // Create Asset
    $(".js-create-asset").click(loadForm);
    $("#modalAssetCreate").on("submit", ".js-asset-create-form", saveForm);

    // Edit Asset
    $(".js-edit-asset").click(loadForm);
    $("#modalAssetEdit").on("submit", ".js-asset-edit-form", saveForm);

    // Delete Asset
    $(".js-delete-asset").click(loadForm);
    $("#modalAssetDelete").on("submit", ".js-asset-delete-form", saveForm);

    // Create Liability
    $(".js-create-liability").click(loadForm);
    $("#modalLiabilityCreate").on("submit", ".js-liability-create-form", saveForm);

    // Edit Liability
    $(".js-edit-liability").click(loadForm);
    $("#modalLiabilityEdit").on("submit", ".js-liability-edit-form", saveForm);

    // Delete Liability
    $(".js-delete-liability").click(loadForm);
    $("#modalLiabilityDelete").on("submit", ".js-liability-delete-form", saveForm);

    // Create Category
    $(".js-create-category").click(loadForm);
    $("#modalCategoryCreate").on("submit", ".js-category-create-form", saveForm);

    // Edit Category
    $(".js-edit-category").click(loadForm);
    $("#modalCategoryEdit").on("submit", ".js-category-edit-form", saveForm);

    // Delete Category
    $(".js-delete-category").click(loadForm);
    $("#modalCategoryDelete").on("submit", ".js-category-delete-form", saveForm);
});
