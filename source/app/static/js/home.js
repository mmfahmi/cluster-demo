document.getElementById('listButton').addEventListener('click', function(){
    console.log('list files');
    loadingOnOff();
    window.location.href ='/home/list';
});

function loadingOnOff(){
    document.querySelector("#listButton").classList.toggle("d-none");
    document.querySelector("#loadingButton").classList.toggle("d-none");
};

function clusterLoadOnOff(){
    document.querySelector("#clusterTargets").classList.toggle("d-none");
    document.querySelector("#clusterButton").classList.toggle("d-none")
};

function folderToCluster(folderName, folderId){;
    console.log(folderName);
    const url =  new URL('/files',window.location.origin);
    url.searchParams.append('folderName', folderName);
    url.searchParams.append('folderId', folderId);
    window.location.href = url;
};

function toggleAllCheckboxes() {
    console.log("toggled")
    var checkboxes = document.querySelectorAll('input[type="checkbox"][name="folderCheck"]');
    checkboxes.forEach(function(checkbox) {
        if (checkbox.style.visibility === 'hidden') {
            checkbox.style.visibility = 'visible';
            checkbox.style.display = 'inline-flex';
        } else {
            checkbox.style.visibility = 'hidden';
            checkbox.style.display = 'none';
        }
    });
}

function selectAll(){
    var selecAll = document.getElementById('selectAll').checked;
    console.log(selecAll); 
    if (selecAll === true){
        var checkboxes = document.querySelectorAll('input[type="checkbox"][name="folderCheck"]');
        checkboxes.forEach(function(checkbox){
            if (checkbox.checked === false){
                checkbox.checked = true;
            } else{
                checkbox.checked = false
            }
        });
    }
};

function listTargets(){
    clusterLoadOnOff();
    const url = new URL('/files/list', window.location.origin);
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="folderCheck"]');
    
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) { // Only process checked checkboxes
            url.searchParams.append('folderName', encodeURIComponent(checkbox.value));
            url.searchParams.append('folderId', encodeURIComponent(checkbox.id));
        }
    });
    
    window.location.href = url;
}
