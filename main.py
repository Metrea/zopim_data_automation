import os
import shutil
import time
import pandas as pd

from glob import glob
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

today = date.today()
files = ['Agent', 'Departments', 'Login', 'Serving', 'Status']
source_path = '{Input Source Path Here}'


def get_data(today):
    if date.today().weekday() == 0:
        today = today
        date_diff = timedelta(3)
        new_date = today - date_diff
        print('Today is Monday, You will need to manually download data')

    else:
        try:
            driver = webdriver.Chrome()

            time.sleep(3)
            analytics = driver.find_element(By.XPATH, "{Xpath to web element}").click()

            time.sleep(3)
            download_button = driver.find_element(By.XPATH, "{Xpath to web element}").click()

            time.sleep(3)
            date_range = driver.find_element(By.XPATH, "{Xpath to web element}").click()
            one_day = driver.find_element(By.XPATH, "{Xpath to web element}").click()

            time.sleep(3)
            send = driver.find_element(By.XPATH, "{Xpath to web element}").click()

            print('Automantion ran successfully')
        except:
            print('Error')

def update_all_files(files, source_path, today):
    for f in files:
        if f == 'Agent':
            new_agent_data = glob(os.path.join(source_path, 'JIC\\' + 'agent_chats_analytics_*.csv'))
            current_agent_path = os.path.join(source_path, 'Data Files\\Agent.csv')
            today = today

            for agent in new_agent_data:
                new_data = pd.read_csv(agent)
                filter_new_data = new_data[new_data.Acceptance.notnull()]
                current_agent_data = pd.read_csv(os.path.join(source_path, 'Data Files\\Agent.csv'))
                append_data = pd.concat([current_agent_data, filter_new_data], ignore_index=True)
                print('Creating new agent data archive...')
                create_new_data_archive = filter_new_data.to_csv(os.path.join(source_path, 'New Data Archive\\' + today.strftime('%Y_%m_%d') + '_' r'new_agent.csv'), index=False)
                print('Updated current agent files...')
                create_current_agent_file = append_data.to_csv(current_agent_path, index=False)
        
        elif f == 'Department':
            new_department_data = glob(os.path.join(source_path, 'JIC\\' + 'department_agent_chats_analytics_*.csv'))
            current_department_path = os.path.join(source_path, 'Data Files\\Agent.csv')
            today = today

            for department in new_department_data:
                new_data = pd.read_csv(department)
                filter_new_data = new_data[new_data.Acceptance.notnull()]
                current_department_data = pd.read_csv(os.path.join(source_path, 'Data Files\\Departments.csv'))
                append_data = pd.concat([current_department_data, filter_new_data], ignore_index=True)
                print('Creating new agent data archive...')
                create_new_data_archive = filter_new_data.to_csv(os.path.join(source_path, 'New Data Archive\\' + today.strftime('%Y_%m_%d') + '_' r'new_department.csv'), index=False)
                print('Updated current department files...')
                create_current_department_file = append_data.to_csv(current_department_path, index=False)
        
        elif f == 'Login':
            new_login_data = glob(os.path.join(source_path, 'JIC\\' + 'login_sessions_*.csv'))
            current_login_path = os.path.join(source_path, 'Data Files\\Login.csv')
            today = today

            for login in new_login_data:
                new_data = pd.read_csv(login)
                current_login_data = pd.read_csv(os.path.join(source_path, 'Data Files\\Login.csv'))
                append_data = pd.concat([current_login_data, new_data], ignore_index=False)
                print('Creating new login data archive...')
                created_new_data_archive = new_data.to_csv(os.path.join(source_path, 'New Data Archive\\' + today.strftime('%Y_%m_%d') + '_' r'new_login.csv'), index=False)
                print('Updated current login file...')
                created_current_login_file = append_data.to_csv(current_login_path, index=False)
        
        elif f == 'Serving':
            new_serving_data = glob(os.path.join(source_path, 'JIC\\' + 'serving_sessions_*.csv'))
            current_serving_path = os.path.join(source_path, 'Data Files\\Serving.csv')
            today = today

            for serving in new_serving_data:
                new_data = pd.read_csv(serving)
                current_serving_data = pd.read_csv(os.path.join(source_path, 'Data Files\\Serving.csv'))
                append_data = pd.concat([current_serving_data, new_data], ignore_index=False)
                print('Creating new serving data archive...')
                created_new_data_archive = new_data.to_csv(os.path.join(source_path, 'New Data Archive\\' + today.strftime('%Y_%m_%d') + '_' r'new_serving.csv'), index=False)
                print('Updated current serving file...')
                created_current_serving_file = append_data.to_csv(current_serving_path, index=False)
        
        elif f == 'Status':
            new_status_data = glob(os.path.join(source_path, 'JIC\\' + 'status_sessions_*.csv'))
            current_serving_path = os.path.join(source_path, 'Data Files\\Status.csv')
            today = today

            for status in new_status_data:
                new_data = pd.read_csv(status)
                current_status_data = pd.read_csv(os.path.join(source_path, 'Data Files\\Status.csv'))
                filter_new_data = new_data.loc[new_data['Status'] != 'offline']
                append_data = pd.concat([current_status_data, filter_new_data], ignore_index=True)
                print('Creating new status data archive...')
                create_new_data_archive = filter_new_data.to_csv(os.path.join(source_path, 'New Data Archive\\' + today.strftime('%Y_%m_%d') + '_' r'new_status.csv'), index=False)
                print('Updated current status file...')
                create_current_status_file = append_data.to_csv(current_status_data, index=False)
        
        else:
            print('Error')


def copy_to_archive(source_path):
    source_active_path = os.path.join(source_path, 'Data Files\\')
    archive_path = os.path.join(source_path, 'Archive\\')
    all_files = os.listdir(source_active_path)
    today = date.today()

    for f in all_files:
        shutil.copyfile(source_path, + f, os.path.join(archive_path, today.strftime('%Y_%m_%d') + '_' + f))
        print('Archiving ' + f)


def delete_new_files(source_path):
    jic_path = os.path.join(source_path, 'JIC\\')
    all_files = os.listdir(jic_path)

    for f in all_files:
        os.remove(jic_path + f)


if __name__ == '__main__':
    start_program = input('Are you ready to get started? (Y/N')
    if start_program in ['Y', 'y']:
        time.sleep(3)
        print('getting_data...')
        get_data()
        print('Check you email and download zip folders, copy filter to ' + source_path)

        run_updates = input('Are you ready to update current files with new data? (Y/N)')
        if run_updates in ['Y', 'y']:
            if os.listdir(source_path + 'JIC\\') == []:
                print('No files in directory')
            else:
                print('Archiving current active files...')
                copy_to_archive(source_path)
                time.sleep(3)
                print('Updating current files...')
                update_all_files(files, source_path, today)
                time.sleep(3)
                print('Finished updating all current files')
                delete_new_files(source_path)
                print('Removed new data files from JIC folder')
                print('Finished! You can now refresh a local copy of the Dashboard.')
    
    else:
        print('Not getting data')

