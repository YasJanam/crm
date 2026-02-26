
//import api from '../api';
//import AdminSidebar from '../admin/admin_sidebar';
import React, { useState } from 'react';
import '../style/sidebar_style.css';
import SalerDealsPage from './deals/dealpage';

function SalerSidebar() {
    const [currentPage,setCurrentPage] = useState('dashboard');

    const menuItems = [
        {
            id:'dashboard',
            label:'داشبورد',
        },
        {
            id:'deals',
            label:'فرصت های فروش',
        },
        {
            id:'leads',
            label:'سرنخ های فروش',
        },
        {
            id:'companies',
            label:'شرکت ها',
        },
        {
            id:'customers',
            label:'مشتریان',
        },
        {
            id:'tasks',
            label:'وظایف',
        },
        {
            id:'interactions',
            label:'تعاملات',
        },
        {
            id:'reminders',
            label:'یادآوری ها',
        },
    ];


    const handleMenuItemClick = (menuid) => {
        setCurrentPage(menuid);
    };



    const renderContent = () => {
        switch(currentPage) {
            case 'dashboard':
                return <></> // SalerDashboardPage
            case 'deals':
                return <SalerDealsPage/> //SalerDealsPage
            case 'leads':
                return <></> //SalerLeadsPage
            case 'companies':
                return <></> // SalerCompaniesPage
            case 'customers':
                return <></> //SalerCustomersPage
            case 'tasks':
                return <></> //SalerTasksPage
            case 'interactions':
                return <></> //SalerInteractionsPage
            case 'reminders':
                return <></> // SalerRemindersPage
            default:
                return <></>    // default page ??
        }
    };


    return (<div className='sidebar_container'>

        <div id='saler-sidebar' className='sidebar'>

        {menuItems.map((menu) => (
            <div
            key={menu.id}
            className='menu-section' 
            >
                <div
                className={`menu-item ${currentPage === menu.id ? 'active' : ''}`}
                onClick={() => handleMenuItemClick(menu.id)}
                >
                    {menu.label}
                   
                </div>
            </div>
        ))}
    </div>


    {/*Saler Content*/}
    <div id="content" className='content'>
        {renderContent()}
    </div>

    </div>);
}

export default SalerSidebar;