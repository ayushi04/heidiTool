// webpack.config.js

module.exports = {
    // other webpack configuration...
  
    module: {
      rules: [
        // other rules...
  
        {
          test: /\.(png|jpg|gif|svg)$/,
          use: [
            {
              loader: 'url-loader',
              options: {
                limit: 8192, // in bytes
                name: '[name].[ext]',
                outputPath: 'images',
              },
            },
          ],
        },
  
        {
          test: /\.(mp4|webm)$/,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: '[name].[ext]',
                outputPath: 'videos',
              },
            },
          ],
        },
  
        // other rules...
      ],
    },
  };
  