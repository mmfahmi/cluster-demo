function clusterFolder(folder_name, folderId){
    console.log('clusterButton:', folder_name);
    const url =  new URL('/files', window.location.origin);
    url.searchParams.append('folderName',folder_name, folderId);
    url.searchParams.append('folderId', folderId);
    window.location.href = url;
};

//TODO: remember to connect this one to the button later
//TODO: give it a real function
function filesToCluster(folder_name, folderId){
    console.log('Clustering');
    const url =  new URL('files/cluster', window.location.origin);
    url.searchParams.append('folderName', folder_name);
    url.searchParams.append('folderId',folderId);
    window.location.href = url;
}

//? waduh. what do i do now from here
function checkType(folderId){
    console.log
}

function upload() {
    console.log("Upload");
    const selectedFiles = document.getElementById('fileInput').files;
    const fileList = document.getElementById('selectedFiles');
    fileList.innerHTML = '';

    for (let i = 0; i < selectedFiles.length; i++) {
        fileList.innerHTML += `<span>${selectedFiles[i].name}</span><br>`;
    }

    // You can handle file upload logic here
}

function resetForm(){
    const fileModal = bootstrap.Modal.getOrCreateInstance("fileModal");
    fileModal.hide();
}