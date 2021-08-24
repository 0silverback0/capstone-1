console.log('im here')

const posts = document.querySelector('.post')

posts.addEventListener('click', (e) => {
    //e.preventDefault()

    let arr = Array.from(e.target.classList)
    if(arr.includes('like')){
        e.preventDefault()
        console.log(e.target.children[0])
        e.target.children[0].setAttribute('class', 'fas fa-thumbs-up')
    }else{
        e.target.children[0].setAttribute('class', 'far fa-thumbs-up')
    }
    
})


const test = async (id) => {
    let res = await axios.get(`/like/${id}`)
}