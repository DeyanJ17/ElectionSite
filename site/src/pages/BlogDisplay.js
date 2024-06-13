import {useState, useEffect} from 'react';

function submitName() {
    alert(document.getElementById("email").value);
}

function getTitle(index) {
    if (index == 0) {
        return "Biden's Declining Latino Support";
    }
    else if (index == 1) {
        return "RFK Jr.'s Momentum Explained";
    }
}

const Blogs = () => {
    const [blogs, setBlogs] = useState([]);

    useEffect(() => {
        const loadBlogs = async () => {
            const blogImports = [];
            for (let i = 1; i <= 2; i++) {
                blogImports.push(import(`./blogs/Blog${i}`));
            }
            const blogModules = await Promise.all(blogImports);

            const blogComponents = blogModules.map(module => module.default);
            setBlogs(blogComponents);
        };
        loadBlogs();
    }, []);

    return (
        <>
            <div className="flex justify-center pt-2">
                <h1>Enter your email address to get blog post notifications</h1>
            </div>
            <div className="flex justify-center pt-2 pb-2">
                <input id="email" type="text" />
                <div className="pl-2">
                    <button onClick={submitName} className="bg-blue-400 p-2">Submit</button>
                </div>
            </div>

            {blogs.map((BlogComponent, index) => (
                <div key={index} className="flex justify-center pt-10 pb-10">
                    <div className="border-2 border-black">
                        <div className="flex justify-center font-bold text-4xl p-2">{getTitle(index)}</div>
                        <div className="flex justify-center pt-2">
                            <div className="h-30 w-80 flex justify-center pb-2"><BlogComponent /></div>
                        </div>        
                    </div>
                </div>
            ))}
        </>
    );
}

export default Blogs;