
import React, { useEffect, useState } from 'react';
import api from '../../api';
import toast, { Toaster } from 'react-hot-toast';
import '../../style/common.css';
import '../../style/company_concats.css';
import '../../style/deal_stage_hist_table.css';
import '../../style/deal_details.css';
/*
    load company-concats
    load deal-stages history
*/

function SalerDealDetails({in_deal,onBack}){
    const [companyConcats,setCompanyConcats] = useState([]);
    const [concatsLoading,setConcatsLoading] = useState(true);

    const [dealStagesHist,setDealStagesHist] = useState([]);
    const [stageHistLoading,setStageHistLoading] = useState(true);

    const [deal,setDeal] = useState(in_deal);
    const [dealLoading,setDealLoading] = useState(true);

    
    const [dealChenge,setDealChanges] = useState(false);
    const [formData,setFormData] = useState({
        title:deal.title,
        amount:deal.amount,
        probability:deal.probability,
        lost_reason:deal.lost_reason,
        expected_close_date:deal.expected_close_date,
    })
 

    const [lostReasonsLoading,setLostReasonsLoading] = useState(true);
    const [lostReasons,setLostReasons] = useState([]);


    const [companyForm,setCompanyForm] = useState({
        name:deal.company.name || '',
        abbreviation:deal.company.abbreviation || '',
        phone:deal.company.phone || '',
        email:deal.company.email || '',
        address:deal.company.address || '',
        type:deal.company.type || '',
        industry:deal.company.industry || '', 
        description:deal.company.description || '',
    });

    const [newConcat,setNewConcat] = useState(false);
    const [concatForm,setConcatForm] = useState({
        role:'',
        name:'',
        phone:'',
        email:''
    });

    const [showStagesHist,setShowStagesHist] = useState(false);
    const [showConcats,setShowConcats] = useState(false);

    useEffect(() => {
        fetchDeal();
    },[dealChenge,]);

    useEffect(() => {
        fetchCompanyConcats();
    },[dealChenge]);

    useEffect(() => {
        fetchDealStagesHistory();
    },[deal]);

    useEffect(() => {
        fetchLostReasons();
    },[]);



    const fetchDeal = async() => {
        try{
            const res = await api.get(`/deals/${in_deal.id}/`);
            setDeal(res.data);
            setDealLoading(false);
        }catch{
            toast.error('error,fetch deal failed');
        }
    }

    const fetchCompanyConcats = async() => {
        try{
            let url =`/company/concats?company_id=${deal.company.id}`;
            const res = await api.get(url);
            setCompanyConcats(res.data);
            setConcatsLoading(false);
        }catch{
            toast.error('خطا در واکشی افراد مرتبط با کمپانی');
        }
    };


    const fetchDealStagesHistory = async() => {
        try{
            let url = `/deal/stages/histories?deal_id=${deal.id}`;
            const res = await api.get(url);
            setDealStagesHist(res.data);
            setStageHistLoading(false);
        }catch{
            toast.error('خطا در واکشی تاریخچه استیج');
        }
    };

    /* ------------ deal details ------------- */

    const changeStage = async(direction) => {
        try{
            if (direction==='front'){
                let url = `/deals/${deal.id}/next-stage/`;
                const res = await api.patch(url);
                setDealChanges(~dealChenge);
            }
            else if(direction==='back'){
                let url = `/deals/${deal.id}/last-stage/`;
                const res = await api.patch(url);
                setDealChanges(~dealChenge);
            }
        }catch(error){
            console.error(error);
            toast.error('خطا در تغییر استیج');
        }
    }


    const openDeal = async() => {
        try{
            const res = await api.post(`/deals/${deal.id}/open/`);
            setDealChanges(~dealChenge);
        }catch{
            toast.error('خطا در باز کردن دیل');
        }
    }

    const winDeal = async() => {
        try{
            const res = await api.post(`/deals/${deal.id}/win/`);
            setDealChanges(~dealChenge);
        }catch{
            toast.error('خطا در ثبت وضعیت موفق');
        }
    }


    const loseDeal = async() => {
        try{
            const res = await api.post(`/deals/${deal.id}/lose/`);
            setDealChanges(~dealChenge);
        }catch{
            toast.error('خطا در ثبت وضعیت ناموفق');
        }
    }

    const fetchLostReasons = async() => {
        try{
            const res = await api.get(`/deal-lost/reasons/`);
            setLostReasons(res.data);
            setLostReasonsLoading(false);
        }catch(error){
            console.error(error)
        }
    }

    /* --------- company -------------- */
    const handleSubmitForm = async() => {
        try{
            const res = await api.patch(`/deals/${deal.id}/`,formData);
            if(res.status>=200 & res.status<300){
                setDealChanges(~dealChenge);
                toast.success('ثبت تغییرات');
            }
        }catch(error){
            console.error(error);
            toast.error('error,edit details failed');
        }
    }
 
    const handleEditCompany = async(e) => {
        try{
            e.preventDefault();
            const res = await api.patch(`/companies/${deal.company.id}/`,companyForm);
            if(res.status>=200 && res.status<300){
                setDealChanges(~dealChenge);
                toast.success('ثبت تغییرات');
            }
        }catch(error){
            console.error(error);
            toast.error('خطا در ثبت تغییرات');
        }
    }

    const onChangeCompanyForm = (e) => {
        const {name,value} = e.target;
        setCompanyForm(prev => ({
            ...prev,
            [name]:value
    }));
    }


    /* ------------ add concat ------------- */
    const handleComcatFormChange = (e) => {
        const {name,value} = e.target;

        setConcatForm(prev => ({
            ...prev,
            [name]:value
        }));
    }

    const handleAddConcat = async(e) => {
        try{
            e.preventDefault();
            if(concatForm.phone===''&&concatForm.email===''){
                toast.error('شماره یا ایمیل را وارد کنید');
                return;
            }
            const res = await api.post('/company/concats/',{
                ...concatForm,
                company_id:deal.company.id
            });
            if(res.status>=200&&res.status<300){
                toast.success('افزودن عضو مرتبط');
                setDealChanges(~dealChenge);
                setTimeout(() => {
                    setNewConcat(false);
                },250);
            }
        }catch{

        }
    }
    
    const handleConcatActivity = async(concat) => {
        try{
            const res = await api.patch(`/company/concats/${concat.id}/`,{
                is_active:!concat.is_active
            });
            setDealChanges(~dealChenge);
            
        }catch{
            toast.error('خطا در فعال/غیرفعال سازی');
        }
    }

    const handleDeleteConcat = async(concat) => {
        try{
            const res = await api.delete(`/company/concats/${concat.id}/`);
            setDealChanges(~dealChenge);
        }catch{

        }
    }
    
    if(dealLoading){
        return <div>loading ...</div>;
    }

    return (<div>
        
        <div className='back-front-actions'>
            <button onClick={onBack}>←</button>
        </div>
        <br></br>



<div style={{display:'flex',gap:'15px',alignItems:'flex-start'}}>

{/* ========================= Deal Details ===================================================*/}

        <div id='deal-details' className='deal-details'>
            <h3>فرصت فروش</h3>

            <br></br>
            <div>
            <div className='deal-details-container'>
                <label>title</label>
                    <input
                    value={formData.title}
                    onChange={(e) => setFormData(prev => ({...prev, title: e.target.value}))}
                    />
                
            </div>


            <div className='deal-details-container'>
                <label>status</label>
                <div className='deal-details-info-row'>
                <p className='deal-details-value'>{deal.status}</p>
                </div>
                <div id='deal-status-actions'>
                    <button
                    onClick={openDeal}
                    className={deal.status==='open'?'button-disable':'open-button'}
                    disabled={deal.status==='open'?true:false}
                    >open</button>
                    <button 
                    onClick={winDeal}
                    className={deal.status==='won'?'button-disable':'win-button'}
                    disabled={deal.status==='won'?true:false}
                    >win (close)</button>
                    <button
                    onClick={loseDeal}
                    className={deal.status==='lost'?'button-disable':'lose-button'}
                    disabled={deal.status==='lost'?true:false}
                    >lose (close)</button>
                </div>
            </div>

          
            <div className='deal-details-container'>
                <label>amount</label>
                    <input
                    value={formData.amount}
                    onChange={(e) => setFormData(prev => ({...prev, amount: e.target.value}))}
                    />
            </div>


            <div className='deal-details-container'>
                <label>probability</label>
                <input
                    value={formData.probability}
                    onChange={(e) => setFormData(prev => ({...prev, probability: e.target.value}))}
                    />
            </div>


        <div className='deal-details-container'>
            <label>currente stage</label>
            <div className='deal-details-info-row'>
                <p>{deal.current_stage?deal.current_stage.name:''}{deal.current_stage?.order?`(${deal.current_stage.order})`:''}</p>
            </div>
            <div>
                <button
                onClick={() => changeStage('back')}
                className={deal.status==='open'?'open-button':'button-disable'}
                disabled={deal.status==='open'?false:true}
                >⇚ last stage</button>
                <button
                onClick={() => changeStage('front')}
                className={deal.status==='open'?'open-button':'button-disable'}
                disabled={deal.status==='open'?false:true}
                >next stage ⇛</button>
            </div>
        </div>
         
            
            {deal.status==='lost'?(<div className='deal-details-container'>
                <label>lost reason</label>
                {/*
                <div className='deal-details-info-row'>
                <p className='deal-details-value'
                >{deal.status==='lost'?deal.lost_reason?deal.lost_reason:'':''}</p>
                </div> */}
                <select className='reasons'
                value={formData.lost_reason} 
                onChange={(e) => setFormData(prev => ({...prev, lost_reason: e.target.value}))}
                >
                    {lostReasonsLoading?'':
                    lostReasons.map((reason) => (
                        <option
                        key={reason.value}
                        value={reason.value} >{reason.label}</option>
                    ))}
                </select>
                </div>): <></>        
        }

         
            <div className='deal-details-container'>
                <label>expected closed date</label>
                    <input
                    value={
                    deal.expected_close_date?(`${new Date(deal.expected_close_date).toLocaleDateString('fa-IR')} (${new Date(deal.expected_close_date).toLocaleTimeString('fa-IR')})`
                    ):''
                    }
                    onChange={(e) => setFormData(prev => ({...prev, expected_close_date: e.target.value}))}
                    />
            </div>

            
            
            <div className='deal-details-container'>
                <label>closed at</label>
                <div id='input-container'>
                    <div className='deal-details-info-row'>
                        <p>
                        {
                        deal.closed_at?(`${new Date(deal.closed_at).toLocaleDateString('fa-IR')} (${new Date(deal.closed_at).toLocaleTimeString('fa-IR')})`
                            ):''}
                        </p>
                    </div>
                </div>
            </div>

            
            <div className='deal-details-container'>
                <label>created_at</label>
                <div id='input-container'>
                    <div className='deal-details-info-row'>
                        <p>
                        {
                        deal.created_at?(`${new Date(deal.created_at).toLocaleDateString('fa-IR')} (${new Date(deal.created_at).toLocaleTimeString('fa-IR')})`
                            ):''}
                        </p>
                    </div>
                </div>
            </div>

            <button onClick={handleSubmitForm} className='open-button'>ذخیره تغییرات</button>
        </div>
        </div>
    


{/* ========================== company ====================================== */}
    {deal.company?(
        <div className='deal-company'>
        <h3>شرکت مربوطه</h3>

        <form onSubmit={handleEditCompany}>
            <div className='deal-company-container'>
                <label>name</label>
                <input value={companyForm.name} name='name' onChange={onChangeCompanyForm} />
            </div>
           

            <div className='deal-company-container'>
                <label>abreviation</label>
                <input value={companyForm.abbreviation} name='abbreviation' onChange={onChangeCompanyForm} />
            </div>
            

            <div className='deal-company-container'>
                <label>phone</label>
                <input value={companyForm.phone} name='phone' onChange={onChangeCompanyForm} />
            </div>

            <div className='deal-company-container'>
                <label>email</label>
                <input value={companyForm.email} name='email' onChange={onChangeCompanyForm} />
            </div>

            <div className='deal-company-container'>
                <label>address</label>
                <input value={companyForm.address} name='address' onChange={onChangeCompanyForm} />
            </div>

            <div className='deal-company-container'>
                <label>industry</label>
                <input value={companyForm.industry} name='industry' onChange={onChangeCompanyForm}/>
            </div>
            


            <div className='deal-company-container'>
               <label>type</label> 
                <select name='type' value={companyForm.type} onChange={onChangeCompanyForm} className='reasons' style={{width:'40%'}}>
                    <option value=''></option>
                    <option value='prospect'>Prospect</option>
                    <option value='customer'>Customer</option>
                </select> 
            </div>


            <div className='deal-company-container'>
                <label>description</label>
                <textarea name='description' onChange={onChangeCompanyForm}>{companyForm.description}</textarea> 
            </div>

            <div style={{margin:'30px'}}>
                <button type='submit' className='open-button'>ثبت تغییرات</button>
                <button type='button' onClick={() => setNewConcat(true)} className='add-concat-btn'>افزودن عضو مرتبط</button>
            </div>
        </form>

        {newConcat?
        (
        <div className='new-concat'>
            <button onClick={() => setNewConcat(false)} className='close-concat-form-btn'>❌️</button>
            <h3>new concat</h3>
        <form onSubmit={handleAddConcat}>
            <div>
                <label>role</label>
                <input name='role' value={concatForm.role} onChange={handleComcatFormChange}/>
            </div>

            <div>
                <label>name</label>
                <input name='name' value={concatForm.name} onChange={handleComcatFormChange}/>
            </div>

            <div>
                <label>phone</label>
                <input name='phone' value={concatForm.phone} onChange={handleComcatFormChange}
                 required={concatForm.email?false:true}
                />
            </div>

            <div>
                <label>email</label>
                <input name='email' value={concatForm.email} onChange={handleComcatFormChange}
                required={concatForm.phone?false:true}/>
            </div>

            <p className='foot-p' hidden={concatForm.phone||concatForm.email?true:false}>شماره یا ایمیل را وارد کنید</p>

            <button type='submit' className='open-button'>ثبت</button>
        </form>
        </div>
        ):<></>
        }

        </div>):<></>}


{/* ============================ stages hist ======================================================== */}

    {stageHistLoading?<></>:(
        dealStagesHist.length?  
        <div className='deal-stages-hist-container' id='deal-stages-history'>
            <h4>تاریخچه استیج</h4>  
            <button onClick={() => setShowStagesHist(!showStagesHist)}
                className='open-close-table'
                >{showStagesHist?'▲':'▼'}</button>
            
            <table>
                <thead>
                    <tr className='deal-stages-hist-table-header-row'>
                        <td>stage</td>
                        <td>entered at</td>
                        <td>exited at</td>
                        {/*<td>lost?</td>*/}
                    </tr>
                </thead>
                <tbody>
                    {showStagesHist?(dealStagesHist.map((stage) => (
                        <tr className='deal-stages-hist-table-row'>
                            <td>{stage.stage.name}({stage.stage.order})</td>
                            <td>
                                {stage.entered_at?(`${new Date(stage.entered_at).toLocaleDateString('fa-IR')} (${new Date(stage.entered_at).toLocaleTimeString('fa-IR')})`)
                                :''}
                            </td>
                            <td>
                                {stage.exited_at?(`${new Date(stage.exited_at).toLocaleDateString('fa-IR')} (${new Date(stage.exited_at).toLocaleTimeString('fa-IR')})`)
                                :'استیج کنونی'}
                            </td>
                            {/*<td>{stage.is_lost?'yes':'no'}</td>*/}
                        </tr>
                    ))):<></>}
                   
                </tbody>
            </table>
        </div>
        : <></> )}
        
</div>



{/* ------------------------------------ company-concats table ---------------------------------- */} 
    {concatsLoading?<></>:
     companyConcats.length?
       <div className='company-concats-table-container' id='company-concats-table'>
            <h4>افراد مرتبط با شرکت</h4>
            <table>
                <thead className='concats-table-header-row'>
                    <tr>
                        <td>role</td>
                        <td>name</td>
                        <td>phone</td>
                        <td>email</td>
                        <td>action?</td>
                        <td>🗑️</td>
                    </tr>
                </thead>
                <tbody>
                    {companyConcats.map((concat) => ( 
                        <tr className='contant-table-row'>
                            <td>{concat.role}</td>
                            <td>{concat.name}</td>
                            <td>{concat.phone}</td>
                            <td>{concat.email}</td>
                            <td><button 
                            className={concat.is_active?'disactive-concat-btn':'active-concat-btn'}
                            onClick={() => handleConcatActivity(concat)}
                            >{concat.is_active?'disactive':'active'}</button></td>
                            <td><button onClick={() => handleDeleteConcat(concat)}
                                className='disactive-concat-btn'>🗑️</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
        :<></> }




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



export default SalerDealDetails;