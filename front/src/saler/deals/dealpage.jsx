
import React, { useEffect, useState } from 'react';
import api from '../../api';
import toast, { Toaster } from 'react-hot-toast';
import '../../style/sidebar_style.css';
import SalerDealDetails from './deal_details';
import '../../style/common.css';


const getStatusCless = (status) => {
    if (status==='open' || status === 'Open'){
        return 'status-open';}

    if (status==='lost' || status==='Lost'){
        return 'status-lost';}

    if (status==='won' || status==='won'){
        return 'status-won'
    }
}

function SalerDealsPage(){
    const [loading,setLoading] = useState(true);
    const [deals,setDeals] = useState([]);
    const [query,setQuery] = useState('');
    const [selectedDeal,setSelectedDeal] = useState(null);
    const [showDealDetails,setShowDealDetails] = useState(false);

    const [dealsChange,setDealsChange] = useState(false);
    /*
    const [filter,setFilters] = useState({
        status:[],
        stage:[],
        amountMax:NaN,
        amountMin:0,

    })*/
    useEffect(() => {
        fetchDeals();
    },[query,dealsChange]);

 

    const fetchDeals = async() => {
        try{
            setLoading(true);
            let url = `/deals?user_id=${localStorage.getItem('user_id')}`;
            if(query !== '') {
                const params = new URLSearchParams();
                params.append('search', query);
                url += `&${params.toString()}`;
            };
            const res = await api.get(url);
            setDeals(res.data);
        }catch(error){
            console.error(error);
            toast.error('خطا در واکشی');
        }finally{
            setLoading(false);
        }
    }

    const onBack = () => {
        setShowDealDetails(false);
        setDealsChange(~dealsChange);
    }

    const onChangeSearch = (e) => {
        const {value} = e.target;
        setQuery(value);
    }

    const onClickDeal = (deal) => {
        setSelectedDeal(deal);
        setShowDealDetails(true);
    }
    /*
    const handleDealsChange = () => {
        setDealsChange(~dealsChange);
    }*/


    if(loading) {
        return (<div>
            ... در حال بارگذاری
        </div>);
    };


    if(selectedDeal && showDealDetails){
        return(<SalerDealDetails
        in_deal={selectedDeal}
        onBack={onBack}
        //dealsChange={handleDealsChange}
        />)
    }


    return (<div>
        <div className='back-front-actions'>
        <button onClick={() => setShowDealDetails(true)}>→</button>
        </div>
        <br></br>

        <div className='table-container'>
            <div className='input-container'>
                <input 
                type="text"  
                key="search-input-deal"
                id="DealSearchInput"
                onChange={(e) => onChangeSearch(e)}
                placeholder="جستجو بر اساس نام  ..." 
                value={query}
                autoFocus
                ></input>
            </div>


            <table>
                <thead>
                    <tr>
                        <td>title</td>
                        <td>company name</td>
                        <td>amount</td>
                        <td>probability</td> 
                        <td>status</td>
                        <td>stage</td>
                        <td>expected close date</td>
                        <td>close date</td>
                        <td>last update date</td>
                        <td>create date</td>
            
                    </tr>
                </thead>
                <tbody>
                    {deals.map((deal) => (
                        <tr onClick={() => onClickDeal(deal)}>
                            
                                <td>{deal.title}</td>
                                <td>{deal.company.name}{deal.company.abbreviation?` (${deal.company.abbreviation})`:''}</td>
                                <td>{deal.amount}</td>
                                <td>{deal.probability}</td> 
                                <td>
                                    <span className={`${getStatusCless(deal.status)}`}>
                                        {deal.status}
                                    </span>
                                </td>
                                <td>
                                {deal.current_stage ? (
                                    `${deal.current_stage.name}(${deal.current_stage.order})`
                                ) : (
                                    ''
                                )}
                                </td>
                                <td>
                                    {deal.expected_close_date?(`${new Date(deal.expected_close_date).toLocaleDateString('fa-IR')} - ${new Date(deal.expected_close_date).toLocaleTimeString('fa-IR')}`)
                                :''}
                                </td>
                                <td>
                                    {deal.closed_at?(`${new Date(deal.closed_at).toLocaleDateString('fa-IR')} - ${new Date(deal.closed_at).toLocaleTimeString('fa-IR')}`
                                ):''}
                                </td>
                                <td>
                                    {deal.updated_at ? (`${new Date(deal.updated_at).toLocaleDateString('fa-IR')} - ${new Date(deal.updated_at).toLocaleTimeString('fa-IR')}` 
                                ): ''}
                                </td>
                                <td>
                                    {deal.created_at ? (`${new Date(deal.created_at).toLocaleDateString('fa-IR')} - ${new Date(deal.created_at).toLocaleTimeString('fa-IR')}` 
                                ): ''}
                                </td>
                                
                                 
                        </tr> 
                              
                    ))}
                </tbody>
            </table>
        </div>

        <Toaster 
            position="top-center"
            reverseOrder={false}
            gutter={8}
            toastOptions={{
            duration: 3000,
            style: {   
                fontSize: '24px',    
                background: '#363636',
                color: '#fff',
                fontFamily: 'IRANSans',
            },
            }}
        />
    </div>);
}

export default SalerDealsPage;