module.exports = {
    lintOnSave: false,
    assetsDir: 'static',  // all webpacked static files will be located at static/ folder
    css: {
        loaderOptions: {
          less: {
            lessOptions: {
              modifyVars: {
                'primary-color': '#918de0',
                'link-color': '#918de0',
                'border-radius-base': '10px',
              },
              javascriptEnabled: true,
            },
          },
        },
      },
}