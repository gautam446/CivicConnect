import React, { useEffect, useState } from "react";
import { Link, Routes, Route, useNavigate } from "react-router-dom";
import api from "./api";

function App() {
  const [user, setUser] = useState(null);
  const [balance, setBalance] = useState(0);
  const navigate = useNavigate();

  async function loadUser() {
    if (!localStorage.getItem("access")) return setUser(null);
    try {
      const res = await api.get("/auth/me/");
      setUser(res.data);
      const rewards = await api.get("/rewards/me/");
      setBalance(rewards.data.balance);
    } catch {
      localStorage.removeItem("access"); localStorage.removeItem("refresh"); setUser(null);
    }
  }
  useEffect(() => { loadUser(); }, []);

  function logout() {
    localStorage.removeItem("access"); localStorage.removeItem("refresh");
    setUser(null); setBalance(0); navigate("/login");
  }
  return <div className="app">
    <header><Link className="brand" to="/">🏙️ CivicConnect</Link>
      <nav>{user ? <><Link to="/">Dashboard</Link><Link to="/complaints/new">New Complaint</Link><Link to="/rewards">Rewards ({balance})</Link><button className="linkbtn" onClick={logout}>Logout</button></> :
      <><Link to="/login">Login</Link><Link to="/register">Register</Link></>}</nav>
    </header>
    <main><Routes>
      <Route path="/" element={user ? <Dashboard user={user} /> : <Landing />} />
      <Route path="/login" element={<Auth mode="login" onDone={loadUser} />} />
      <Route path="/register" element={<Auth mode="register" onDone={loadUser} />} />
      <Route path="/complaints/new" element={<Protected user={user}><NewComplaint refresh={loadUser}/></Protected>} />
      <Route path="/rewards" element={<Protected user={user}><Rewards refresh={loadUser}/></Protected>} />
      <Route path="*" element={<Landing />} />
    </Routes></main>
    <footer>CivicConnect · Report civic issues. Track progress. Earn community rewards.</footer>
  </div>;
}

function Protected({ user, children }) { return user ? children : <p className="notice">Please log in to continue.</p>; }
function Landing() {
  return <section className="hero"><div><span className="eyebrow">COMMUNITY • ACTION • IMPACT</span><h1>Make your neighbourhood<br/><em>better, together.</em></h1>
    <p>Report local issues, follow their progress and earn points for verified community contributions.</p>
    <Link className="primary" to="/register">Get started</Link></div>
    <div className="hero-card"><div className="bigicon">🌱</div><h3>Small actions. Real impact.</h3><p>Roads · Water · Garbage · Drainage · Electricity</p></div></section>;
}
function Auth({ mode, onDone }) {
  const [form, setForm] = useState({ username:"", password:"", email:"", first_name:"", last_name:"", phone:"", address:"" });
  const [error, setError] = useState(""); const navigate = useNavigate();
  const change = e => setForm({...form, [e.target.name]:e.target.value});
  async function submit(e) {
    e.preventDefault(); setError("");
    try {
      if (mode === "register") await api.post("/auth/register/", form);
      const res = await api.post("/auth/login/", {username:form.username, password:form.password});
      localStorage.setItem("access", res.data.access); localStorage.setItem("refresh", res.data.refresh);
      await onDone(); navigate("/");
    } catch (err) {
      const data = err.response?.data;
      setError(data ? Object.entries(data).map(([k,v])=>`${k}: ${Array.isArray(v)?v.join(", "):v}`).join(" | ") : "Cannot connect to server.");
    }
  }
  return <section className="form-card"><h2>{mode === "login" ? "Welcome back" : "Create your account"}</h2><p className="muted">{mode === "login" ? "Log in to manage your civic contributions." : "Join your community and make a difference."}</p>
    <form onSubmit={submit}>
      <label>Username<input name="username" value={form.username} onChange={change} required /></label>
      {mode === "register" && <><label>Email<input type="email" name="email" value={form.email} onChange={change} required /></label>
      <div className="row"><label>First name<input name="first_name" value={form.first_name} onChange={change}/></label><label>Last name<input name="last_name" value={form.last_name} onChange={change}/></label></div>
      <label>Mobile number<input name="phone" value={form.phone} onChange={change}/></label><label>Address<input name="address" value={form.address} onChange={change}/></label></>}
      <label>Password<input type="password" name="password" value={form.password} onChange={change} required minLength="8"/></label>
      {error && <div className="error">{error}</div>}<button className="primary full">{mode === "login" ? "Login" : "Register"}</button>
    </form>
  </section>;
}
function Dashboard({ user }) {
  const [items,setItems] = useState([]); const [err,setErr] = useState("");
  useEffect(()=>{api.get("/complaints/").then(r=>setItems(r.data.results || r.data)).catch(()=>setErr("Unable to load complaints."));},[]);
  return <><div className="pagehead"><div><span className="eyebrow">YOUR COMMUNITY</span><h1>Hello, {user.first_name || user.username} 👋</h1><p className="muted">Here is your complaint activity.</p></div><Link className="primary" to="/complaints/new">＋ Report an issue</Link></div>
    <div className="stats"><div><span>My complaints</span><strong>{items.length}</strong></div><div><span>Resolved</span><strong>{items.filter(x=>x.status==="resolved").length}</strong></div><div><span>Open</span><strong>{items.filter(x=>!["resolved","rejected"].includes(x.status)).length}</strong></div></div>
    <section className="panel"><h2>Recent complaints</h2>{err && <p className="error">{err}</p>}{items.length===0 ? <p className="muted">No complaints yet. Report your first issue.</p> : <div className="tablewrap"><table><thead><tr><th>Issue</th><th>Category</th><th>Location</th><th>Status</th><th>Submitted</th></tr></thead><tbody>{items.map(x=><tr key={x.id}><td>#{x.id} · {x.title}</td><td>{x.category_name}</td><td>{x.location}</td><td><span className={`badge ${x.status}`}>{x.status.replace("_"," ")}</span></td><td>{new Date(x.created_at).toLocaleDateString()}</td></tr>)}</tbody></table></div>}</section>
  </>;
}
function NewComplaint({ refresh }) {
  const [cats,setCats]=useState([]); const [form,setForm]=useState({title:"",category:"",description:"",location:"",image:null}); const [msg,setMsg]=useState(""); const [error,setError]=useState("");
  const navigate=useNavigate();
  useEffect(()=>{api.get("/categories/").then(r=>{const d=r.data.results||r.data;setCats(d);if(d.length)setForm(f=>({...f,category:d[0].id}));}).catch(()=>setError("Could not load categories."));},[]);
  function change(e){setForm({...form,[e.target.name]:e.target.name==="image"?e.target.files[0]:e.target.value});}
  async function submit(e){e.preventDefault();setError("");const data=new FormData();Object.entries(form).forEach(([k,v])=>{if(v!==null&&v!=="")data.append(k,v);});
    try{await api.post("/complaints/",data,{headers:{"Content-Type":"multipart/form-data"}});setMsg("Complaint submitted successfully.");await refresh();setTimeout(()=>navigate("/"),700);}
    catch(err){setError(JSON.stringify(err.response?.data||"Unable to submit complaint."));}}
  return <section className="form-card wide"><h2>Report a civic issue</h2><p className="muted">Provide clear details so the responsible team can investigate.</p><form onSubmit={submit}>
    <label>Complaint title<input name="title" value={form.title} onChange={change} required maxLength="160"/></label>
    <label>Category<select name="category" value={form.category} onChange={change} required>{cats.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}</select></label>
    <label>Description<textarea name="description" value={form.description} onChange={change} rows="4" required/></label>
    <label>Location / address<input name="location" value={form.location} onChange={change} required placeholder="Area, street, landmark"/></label>
    <label>Photo (optional)<input type="file" name="image" accept="image/*" onChange={change}/></label>
    {msg&&<p className="success">{msg}</p>}{error&&<p className="error">{error}</p>}<button className="primary">Submit complaint</button>
  </form></section>;
}
function Rewards({ refresh }) {
  const [data,setData]=useState({balance:0,transactions:[],redemptions:[]});const [catalog,setCatalog]=useState([]);const [leader,setLeader]=useState([]);const [msg,setMsg]=useState("");const [error,setError]=useState("");
  async function load(){const [a,b,c]=await Promise.all([api.get("/rewards/me/"),api.get("/rewards/"),api.get("/leaderboard/")]);setData(a.data);setCatalog(b.data.results||b.data);setLeader(c.data);}
  useEffect(()=>{load().catch(()=>setError("Unable to load rewards."));},[]);
  async function redeem(id){setMsg("");setError("");try{const r=await api.post("/rewards/redeem/",{reward_id:id});setMsg(`Redeemed! Your demo coupon code: ${r.data.redemption.coupon_code}`);await load();await refresh();}catch(e){setError(e.response?.data?.detail||"Redemption failed.");}}
  return <><div className="pagehead"><div><span className="eyebrow">COMMUNITY REWARDS</span><h1>Your points & rewards</h1></div><div className="points"><strong>{data.balance}</strong><span>POINTS</span></div></div>
    {msg&&<p className="success">{msg}</p>}{error&&<p className="error">{error}</p>}
    <section className="panel"><h2>Available rewards</h2><div className="rewardgrid">{catalog.map(r=><article className="reward" key={r.id}><div className="gift">🎁</div><h3>{r.title}</h3><p className="muted">{r.description}</p><strong>{r.points_required} points</strong><button className="primary full" disabled={data.balance<r.points_required} onClick={()=>redeem(r.id)}>Redeem</button></article>)}</div></section>
    <section className="panel"><h2>Leaderboard</h2>{leader.length===0?<p className="muted">No points earned yet.</p>:leader.map((x,i)=><div className="leader" key={x.username}><span>{i+1}. {x.username}</span><strong>{x.points} pts</strong></div>)}</section>
    <section className="panel"><h2>Points history</h2>{data.transactions.length===0?<p className="muted">No transactions yet. Verified complaints earn points.</p>:data.transactions.map(t=><div className="leader" key={t.id}><span>{t.description}</span><strong>{t.transaction_type==="earned"?"+":"-"}{t.points}</strong></div>)}</section>
    <section className="panel"><h2>My coupon codes</h2>{data.redemptions.length===0?<p className="muted">No coupons redeemed yet.</p>:data.redemptions.map(r=><div className="leader" key={r.id}><span>{r.reward_title}</span><code>{r.coupon_code}</code></div>)}</section>
  </>;
}
export default App;
