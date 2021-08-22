console.log('im here')

async function test(){
    let res = await axios.get('/artist/', params={id: 118, apikey: 'c6616ea169eda990ca4e9f3bc7e17b5c'})
    console.log(res.data)
}


test()

const tester = () => {
    console.log('wtf')
}