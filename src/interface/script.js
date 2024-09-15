
let newbill = new Map();

document.addEventListener('DOMContentLoaded', function (){
    const itemsearch_inputdiv = document.getElementById("itemsearch_input");

    itemsearch_inputdiv.addEventListener('input', function() {
        var itemsearchcrit = itemsearch_inputdiv.value;
        if (itemsearchcrit.trim() == "") {
            loadItemsListFend();
        } else{
            itemSearchFendBend(itemsearchcrit);
        }
    });

    newbill = new Map();

    loadItemsListFend();
    setTodate();
});

async function addNewItem(){
    const add_form = document.getElementById("newitemform");
    if(add_form.checkValidity()){
        var itemname = document.getElementById("newitemname_input").value;
        var itemunit = document.getElementById("newitemunit_input").value;
        var itemminqty = document.getElementById("newitemminqty_input").value;
        let addto_invdb = await eel.addItemToInv(itemname, itemunit, itemminqty)();
        alert(addto_invdb);
        document.getElementById("newitemminqty_input").value = "";
        document.getElementById("newitemunit_input").value = "";
        document.getElementById("newitemname_input").value = "";
        loadItemsListFend();
        return 
    } else{
        add_form.reportValidity();
        return
    }
}

async function printRequisition(){
    let printslip = await eel.gen_reqslip_print()();
    return
}

function newItemShowModal(){
    var modalelem1 = document.getElementById("modalOverlay1");
    modalelem1.style.display = "flex";
}

async function generateRequisition() {
    var requisitiondets = await eel.create_requisition_slip()();
    var reqmodal = document.getElementById("modalOverlay");
    reqmodal.style.display = "flex";
    var reqlistelem = document.getElementById("reqlist");
    reqlistelem.innerHTML = "";
    var reqtext = "";
    requisitiondets.forEach(element => {
        reqtext += element + "<br>";
    });
    reqlistelem.innerHTML = reqtext;
}

async function setTodate(){
    let todate = await eel.getTodate()();
    const todate_element = document.getElementById("date_input");
    todate_element.textContent = todate;
}

async function addCurrentToInventory(){
    var objectlist = [];
    newbill.keys().forEach(itemkey => {
        var this_itemarr = newbill.get(itemkey);
        this_itemarr.push(itemkey);
        objectlist.push(this_itemarr);
    });
    var addtoinvretmsg = await eel.addToInv(objectlist)();
    if (addtoinvretmsg == "success"){
        alert("Added Items To Inventory");
        newbill = new Map();
        document.getElementById("billsummaryparentact").innerHTML = "";
        loadItemsListFend();
    } else{
        alert("Failed to Add To Inventory");
    }
}

async function removeCurrentFromInventory(){
    var objectlist = [];
    newbill.keys().forEach(itemkey => {
        var this_itemarr = newbill.get(itemkey);
        this_itemarr.push(itemkey);
        objectlist.push(this_itemarr);
    });
    var addtoinvretmsg = await eel.removeFromInv(objectlist)();
    if (addtoinvretmsg == "success"){
        alert("Removed Items From Inventory");
        newbill = new Map();
        document.getElementById("billsummaryparentact").innerHTML = "";
        loadItemsListFend();
    } else{
        alert("Failed to Add To Inventory: " + addtoinvretmsg);
    }
}

function set_fend_to_dictvalues(focusid=null){
    // fix_newbill_itemorder();
    // updateSumTotalFendBend();
    var billsummaryparentcont = document.getElementById("billsummaryparentact");
    billsummaryparentcont.innerHTML = "";
    newbill.keys().forEach(itemkey => {
        var itemarray = [itemkey, newbill.get(itemkey)[0], newbill.get(itemkey)[1], newbill.get(itemkey)[2], newbill.get(itemkey)[3]];
        addToSummary(itemarray);
    });
    if(focusid!=null){
        document.getElementById(focusid).focus();
    }
}


function addToSummary(itemdets_arr){
    var summaryparentcont = document.getElementById("billsummaryparentact");
    
    var newitem_contdiv = document.createElement("div");
    newitem_contdiv.className = "billeditem_cont";
    newitem_contdiv.id = itemdets_arr[0] + "newitemcontdiv";

    var newitem_slno = document.createElement("div");
    newitem_slno.className = "slno_billsummary_class";
    newitem_slno.textContent = itemdets_arr[0];

    var newitem_itemname = document.createElement("div");
    newitem_itemname.className = "itemname_billsummary_class";
    newitem_itemname.textContent = itemdets_arr[1];

    var newitem_itemqty = document.createElement("div");
    newitem_itemqty.className = "qty_billsummary_class";
    var newitem_qty_tbox = document.createElement("input");
    newitem_qty_tbox.type = "number";
    newitem_qty_tbox.step = "0.01";
    newitem_qty_tbox.id = "qty_bill_input_" + itemdets_arr[0]
    newitem_qty_tbox.className = "text-input-qty_billsummary";
    newitem_qty_tbox.value = itemdets_arr[3];
    // var item_in_bill = newbill.get(itemdets_arr[0]);
    // item_in_bill[2] = parseFloat(itemdets_arr[3]).toFixed(2);;
    // newbill.set(itemdets_arr[0], item_in_bill);
    newitem_qty_tbox.addEventListener('input', function() {
        if (newitem_qty_tbox.value.trim() != "") {
            var new_qty = newitem_qty_tbox.value.trim();
            var item_innewbill = newbill.get(itemdets_arr[0]);
            item_innewbill[2] = new_qty;
            // item_innewbill[4] = item_innewbill[2] * item_innewbill[3];
            newbill.set(itemdets_arr[0], item_innewbill);
            // set_fend_to_dictvalues(focusid="qty_bill_input_"+itemdets_arr[0]);

        }
    });


    // newitem_qty_tbox.addEventListener('blur', (event) => {
    //     const value = parseFloat(event.target.value).toFixed(2);

    //     if (!isNaN(value)) {
    //         // Format to two decimal places
    //         event.target.value = value
    //         var item_in_bill = newbill.get(itemdets_arr[0]);
    //         item_in_bill[2] = value;
    //         newbill.set(itemdets_arr[0], item_in_bill);
    //         set_fend_to_dictvalues();
    //     }
    // });
    newitem_itemqty.appendChild(newitem_qty_tbox);

    var newitem_itemamount = document.createElement("div");
    newitem_itemamount.className = "amount_billsummary_class";
    var newitem_amount_tbox = document.createElement("input");
    newitem_amount_tbox.type = "text";
    newitem_amount_tbox.id = "amount_bill_input_" + itemdets_arr[0]
    newitem_amount_tbox.className = "text-input-qty_billsummary";
    newitem_amount_tbox.value = itemdets_arr[4];
    newitem_amount_tbox.readOnly = true;
    newitem_itemamount.appendChild(newitem_amount_tbox);

    var newitem_removeitem_div = document.createElement("div");
    newitem_removeitem_div.className = "delitem_billsummary_class";
    newitem_removeitem_div.textContent = "Remove";
    newitem_removeitem_div.onclick = function(){
        remove_from_bill(itemdets_arr[0]);
    };

    newitem_contdiv.appendChild(newitem_slno);
    newitem_contdiv.appendChild(newitem_itemname);
    // newitem_contdiv.appendChild(newitem_itemrate);
    newitem_contdiv.appendChild(newitem_itemqty);
    newitem_contdiv.appendChild(newitem_itemamount);
    newitem_contdiv.appendChild(newitem_removeitem_div);

    summaryparentcont.appendChild(newitem_contdiv);
    
}

function remove_from_bill(itemid){
    // var summaryparentcont = document.getElementById("billsummaryparentact");
    // var itemcontdiv = document.getElementById(remove_itemid + "newitemcontdiv");
    // summaryparentcont.removeChild(itemcontdiv);
    // itemcount = itemcount - 1;
    newbill.delete(itemid);
    // fix_newbill_itemorder();
    set_fend_to_dictvalues();
}


async function pushToBill(itemid){
    if(!newbill.has(itemid)){
        let defaultdets = await eel.getDefaultDets(itemid)();
        // itemcount = itemcount + 1;
        newbill.set(itemid, [defaultdets[1], defaultdets[2], defaultdets[2], defaultdets[3]]);
        // 1 name, 2 minqty, 3 unit
        set_fend_to_dictvalues();
    }
}

async function loadItemsListFend(){
    const itemsearch_inputdiv1 = document.getElementById("itemsearch_input");
    if (itemsearch_inputdiv1.value != ""){
        itemSearchFendBend(itemsearch_inputdiv1.value);
        return
    }
    
    let itemslist = await eel.getAllItemsList()();
    var menuitemslist = document.getElementById("itemslist_filtered")
    menuitemslist.innerHTML = "";
    itemslist.forEach(itemtext => {
        newitemdiv = document.createElement("div");
        newitemdiv.textContent = itemtext;
        newitemdiv.className = "menulist-itemclass";
        newitemdiv.id = itemtext.split(" ")[0].trim();
        newitemdiv.onclick = function(){
            pushToBill(itemtext.split(" ")[0].trim());
        };
        menuitemslist.appendChild(newitemdiv);
    });
    return
}

async function itemSearchFendBend(searchcrit){
    let searchres = await eel.searchitems(searchcrit)();
    var menuitemslist = document.getElementById("itemslist_filtered")
    menuitemslist.innerHTML = "";
    searchres.forEach(itemtext => {
        newitemdiv = document.createElement("div");
        newitemdiv.textContent = itemtext;
        newitemdiv.className = "menulist-itemclass";
        newitemdiv.id = itemtext.split(" ")[0].trim();
        newitemdiv.onclick = function(){
            pushToBill(itemtext.split(" ")[0].trim());
        };
        menuitemslist.appendChild(newitemdiv);
    });
    return
}