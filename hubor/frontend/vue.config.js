module.exports = {
    lintOnSave: false,
    assetsDir: 'static',  // all webpacked static files will be located at static/ folder
    css: {
        loaderOptions: {
          less: {
            lessOptions: {
              modifyVars: {
                
              },
              javascriptEnabled: true,
            },
          },
        },
      },
}