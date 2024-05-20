import {useState, useEffect} from 'react';

function submitName() {
    alert(document.getElementById("email").value);
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
            {blogs.map((BlogComponent, index) => (
                <div key={index} className="flex justify-center pt-10 pb-10">
                    <div>
                        <div className="flex justify-center font-bold text-4xl">Post {index + 1}</div>
                        <div className="flex justify-center pt-2"></div>        
                        <div className="h-30 w-80 flex justify-center"><BlogComponent /></div>
                    </div>
                </div>
            ))}

            <div className="flex justify-center">
                <h1>Enter your email address to get blog post notifications</h1>
            </div>
            <div className="flex justify-center pt-2 pb-2">
                <input id="email" type="text" />
                <div className="pl-2">
                    <button onClick={submitName} className="bg-blue-400 p-2">Submit</button>
                </div>
            </div>
        </>
    );
}

export default Blogs;