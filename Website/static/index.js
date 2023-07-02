function deleteNote(id){
    fetch('/delete-job', {
        method: 'POST',
        body: JSON.stringify({jobId : id})
    }).then( 
        (_res) => {
            window.location.href = "/company"
        }
    )
    
}
function viewApplicants(id){
    window.location.href = `/viewCandidates/${id}`
}

function applyJob(id){
    fetch('/apply-job', {
        method : 'POST',
        body: JSON.stringify({jobId : id})
    }).then(
        (_res) => {
            window.location.href = "/applicant"
            console.log("Applied to job successfully")
            console.log("Response-> ", _res)
        }
    )
}

