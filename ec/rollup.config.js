import resolve from 'rollup-plugin-node-resolve';

export default {
    input: 'app/static/app/js/index.js',
    output: {
        file: 'app/static/src/bundle.js',
        format: 'cjs',
		sourcemap: true,
    },
    plugins: [
        resolve(),
    ],
};
