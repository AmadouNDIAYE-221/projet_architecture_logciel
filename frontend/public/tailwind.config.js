module.exports = {
  content: [
    './*.html',
    './js/**/*.js',       // ← très important
  ],
  safelist: [
    'text-blue-600',
    'text-red-600',
    'text-white',
    'hover:text-gray-300',
    'hover:text-blue-800',
    'hover:underline',
    'font-medium'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
