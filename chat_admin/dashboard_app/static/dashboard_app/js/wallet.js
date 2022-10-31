// const db_url='https://api.afrometa.co/';
const db_url= `${window.location.origin}/api/v1/`;

document.getElementById("set-default").addEventListener("click", async()=>{
    await postactiveType('default');
    await sendRequestDefault();
});

document.getElementById("set-nft").addEventListener("click", async()=>{
    await postactiveType('nft');
    await sendRequestDefault();
});
document.getElementById("set-disabled").addEventListener("click", async()=>{
    await postactiveType('disabled');
    await sendRequestDefault();
});



async function addNFT(){
    const nftAddress=document.getElementById("nft-input").value;
    let url=`${db_url}wallet-whitelist-add/`;

    if(nftAddress){
        await fetch(url,{
            method:'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
            body: JSON.stringify({
                nftAddress
            })
        });
    }
    document.getElementById("nft-input").value="";
    await sendRequestDefault();

}

async function removeNFT(nft){
    const nftAddress=nft;
    let url=`${db_url}wallet-whitelist-remove/`;
    if(nftAddress){
        await fetch(url,{
            method:'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
            body: JSON.stringify({
                nftAddress
            })
        });
    }
    await sendRequestDefault();

}

async function sendRequestDefault(){

   let url=`${db_url}wallet-status/`;
   const req=await fetch(url);
   const res=await req.json();
   document.getElementById("wallet-active-status").innerText=res.wallet.activeType;
   createTable([]);
   createTable(res.wallet.whitelist);

}
async function postactiveType(type){

    let url=`${db_url}wallet-status/`;
    await fetch(url,{
        method:'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            activeType:type
        })
    });
 }
sendRequestDefault();

function createTable(tableData) {
    var table = document.getElementById('nft-table');
    var tableBody = document.getElementById('nft-table-tbody');
    if(tableData.length>0){


        tableData.forEach(function(rowData) {
          var row = document.createElement('tr');

          var cell = document.createElement('td');
          cell.appendChild(document.createTextNode(rowData));
          row.appendChild(cell);
          row.innerHTML+=`<td><button onclick="removeNFT('${rowData}')" id="set-disabled" class="btn btn-danger btn-sm mr-2">Remove</button></td>`;

          tableBody.appendChild(row);
        });

        table.appendChild(tableBody);
    }
    else{
        while (tableBody.hasChildNodes()) {
            tableBody.removeChild(tableBody.lastChild);
          }
    }


  }
