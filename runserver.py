from api import create_app
# from api.config.config import config_dict

# app = create_app(config_app=config_dict['prod'])
app = create_app()

if __name__ == '__main__':
  app.run()