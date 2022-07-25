class StorageTool{
    constructor(){
        this.storeName = "st_"
    }
    
}
const storageProxy = (function(){
    let instance = null
    return function(){
        if(!instance){
            instance = new StorageTool()
        }
        return instance
    }
})()

export default storageProxy